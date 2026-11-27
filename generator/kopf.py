"""Kopfbild: dunkler Filmstreifen mit einem Bild je Woche, der Name steht auf der Kante."""
from .schrift import pfad, saira
from .stil import FILM, PAPIER, belichtung_css, filmstreifen, svg

BREITE, HOEHE, KANTE = 1600, 460, 250
UNTERZEILE = "Photos from the trail, code from the desk."


def _mehrzahl(n, wort):
    return f"{n:,} {wort}" if n == 1 else f"{n:,} {wort}S"


def kopf(stufen, beitraege, tage, thema):
    anzeige, klein, zeile = saira(900, 50), saira(600, 75), saira(400, 100)
    name, _ = pfad(anzeige, "Daxidfoto", 230, 50, 342, sperr=-0.015)
    unter, _ = pfad(zeile, UNTERZEILE, 34, BREITE - 56, 318, anker="end")
    stat, _ = pfad(klein, f"{_mehrzahl(beitraege, 'CONTRIBUTION')} ON {_mehrzahl(tage, 'DAY')}",
                   24, BREITE - 56, 364, sperr=0.04, anker="end")
    hinweis, _ = pfad(klein, "ONE FRAME PER WEEK, LAST 12 MONTHS", 19, BREITE - 56, 394, sperr=0.04, anker="end")
    teile = [
        belichtung_css(),
        f'<clipPath id="karte"><rect width="{BREITE}" height="{HOEHE}" rx="18"/></clipPath>',
        f'<clipPath id="oben"><rect width="{BREITE}" height="{KANTE}"/></clipPath>',
        f'<clipPath id="unten"><rect y="{KANTE}" width="{BREITE}" height="{HOEHE - KANTE}"/></clipPath>',
        '<g clip-path="url(#karte)">',
        f'<rect width="{BREITE}" height="{HOEHE}" fill="{thema.grund}"/>',
        filmstreifen(0, 0, BREITE, KANTE, stufen, klein),
        f'<path d="{name}" fill="{PAPIER}" stroke="{FILM}" stroke-width="14" stroke-linejoin="round" '
        f'paint-order="stroke" clip-path="url(#oben)"/>',
        f'<path d="{name}" fill="{thema.name_unten}" clip-path="url(#unten)"/>',
        f'<path d="{unter}" fill="{thema.leise}"/>',
        f'<path d="{stat}" fill="{thema.akzent}"/>',
        f'<path d="{hinweis}" fill="{thema.akzent}" opacity=".7"/>',
        "</g>",
    ]
    return svg(BREITE, HOEHE, "".join(teile), f"Daxidfoto – {UNTERZEILE}")
