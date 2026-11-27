"""Beitragsraster von GitHub lesen und zu Wochen zusammenfassen.

Die Leselogik stammt aus daxidfoto.de (server/github_balken.py). Die öffentliche Seite zählt private
Beiträge als Zahl mit, ohne Repo-Namen, und braucht keinen Token.
"""
import datetime as dt
import html.parser
import re
import urllib.request

ADRESSE = "https://github.com/users/Divad27/contributions"
MIN_TAGE = 360
_ANZAHL = re.compile(r"^(\d[\d,]*) contributions? on ")


class _Leser(html.parser.HTMLParser):
    """Sammelt die Tageszellen (<td data-date data-level id>) und die Texte der zugehörigen <tool-tip for=id>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.zellen = {}
        self.texte = {}
        self._tip = None
        self._puffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and a.get("data-date") and a.get("data-level") is not None and a.get("id"):
            self.zellen[a["id"]] = (a["data-date"], a["data-level"])
        elif tag == "tool-tip" and a.get("for"):
            self._tip = a["for"]
            self._puffer = []

    def handle_data(self, data):
        if self._tip is not None:
            self._puffer.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self._tip is not None:
            self.texte[self._tip] = "".join(self._puffer).strip()
            self._tip = None


def anzahl_aus_text(text):
    """'No contributions on …' → 0, '3 contributions on …' → 3, '1,204 contributions on …' → 1204."""
    if text.startswith("No contributions on "):
        return 0
    treffer = _ANZAHL.match(text)
    if not treffer:
        raise ValueError(f"Unbekannter Text im Raster: {text!r}")
    return int(treffer.group(1).replace(",", ""))


def pruefe(tage):
    """Wirft ValueError, wenn die Tage nicht lückenlos, zu wenige oder in sich widersprüchlich sind."""
    if len(tage) < MIN_TAGE:
        raise ValueError(f"Nur {len(tage)} Tage gefunden, erwartet mindestens {MIN_TAGE}")
    vorher = None
    for datum, anzahl, stufe in tage:
        tag = dt.date.fromisoformat(datum)
        if vorher is not None and tag - vorher != dt.timedelta(days=1):
            raise ValueError(f"Lücke oder Doppelung vor {datum}")
        if not 0 <= stufe <= 4:
            raise ValueError(f"Stufe {stufe} am {datum} außerhalb von 0 bis 4")
        if (stufe == 0) != (anzahl == 0):
            raise ValueError(f"Stufe {stufe} passt nicht zu {anzahl} Beiträgen am {datum}")
        vorher = tag


def lese(html_text):
    """Nach Datum sortierte Liste [datum, anzahl, stufe], geprüft."""
    leser = _Leser()
    leser.feed(html_text)
    tage = []
    for zelle, (datum, stufe) in leser.zellen.items():
        if zelle not in leser.texte:
            raise ValueError(f"Kein Text zur Zelle {zelle}")
        tage.append([datum, anzahl_aus_text(leser.texte[zelle]), int(stufe)])
    tage.sort(key=lambda t: t[0])
    pruefe(tage)
    return tage


def hole(adresse=ADRESSE):
    anfrage = urllib.request.Request(adresse, headers={"User-Agent": "github-profile-readme"})
    with urllib.request.urlopen(anfrage, timeout=20) as antwort:
        return antwort.read().decode("utf-8")


def wochen(tage, anzahl=52):
    """Beiträge je Woche (ab Montag), die letzten `anzahl` Wochen, älteste zuerst."""
    summen = {}
    for datum, n, _ in tage:
        tag = dt.date.fromisoformat(datum)
        montag = tag - dt.timedelta(days=tag.weekday())
        summen[montag] = summen.get(montag, 0) + n
    return [summen[m] for m in sorted(summen)][-anzahl:]


def stufen(summen):
    """0 = keine Beiträge, 1 bis 4 nach den Quartilen der Wochen mit Beiträgen."""
    belegt = sorted(s for s in summen if s)
    if not belegt:
        return [0] * len(summen)
    grenzen = [belegt[int(len(belegt) * q)] for q in (0.25, 0.5, 0.75)]
    return [0 if s == 0 else 1 + sum(s > g for g in grenzen) for s in summen]


def jahr(tage):
    """(Beiträge, Tage mit Beiträgen) der letzten 365 Tage."""
    letzte = tage[-365:]
    return sum(t[1] for t in letzte), sum(1 for t in letzte if t[1])
