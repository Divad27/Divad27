"""Farben und Bausteine im Look von daxidfoto.de."""
from dataclasses import dataclass
from xml.sax.saxutils import escape

from .schrift import pfad

FILM, PERFO, PAPIER = "#0E1330", "#2A3366", "#EEF0F6"
ULTRA, ORANGE, LAVENDEL = "#2C3FCB", "#E9A23B", "#8D9CFF"
UNBELICHTET = "#1B2350"
BILD = (UNBELICHTET, ULTRA, "#5566E0", LAVENDEL, PAPIER)


@dataclass(frozen=True)
class Thema:
    name: str
    grund: str
    text: str
    name_unten: str
    leise: str
    akzent: str


HELL = Thema("hell", grund=PAPIER, text="#141B3D", name_unten="#141B3D", leise="#4A5072", akzent=ULTRA)
DUNKEL = Thema("dunkel", grund="#141B3D", text=PAPIER, name_unten=LAVENDEL, leise="#AEB4DA", akzent=LAVENDEL)
THEMEN = (HELL, DUNKEL)


def svg(breite, hoehe, inhalt, titel):
    t = escape(titel, {'"': "&quot;"})
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breite} {hoehe}" width="{breite}" height="{hoehe}" '
            f'role="img" aria-label="{t}"><title>{t}</title>{inhalt}</svg>')


def belichtung_css(schritt=0.035):
    """Jedes Bild startet unbelichtet und bekommt seine Farbe, um schritt Sekunden je Index --i versetzt."""
    stufen = "".join(f".s{i}{{fill:{farbe}}}" for i, farbe in enumerate(BILD))
    return (f"<style>{stufen}"
            f".b{{animation:belichten .7s ease-out both;animation-delay:calc(var(--i)*{schritt}s + .3s)}}"
            f"@keyframes belichten{{from{{fill:{UNBELICHTET}}}}}</style>")


def perforation(x, y, breite, hoehe, loch_b, loch_h, rand):
    """Filmgrund mit je einer Lochreihe oben und unten."""
    teile = [f'<rect x="{x}" y="{y}" width="{breite}" height="{hoehe}" fill="{FILM}"/>']
    anzahl = int(breite / (loch_b * 2.2))
    abstand = breite / anzahl
    for i in range(anzahl):
        lx = x + i * abstand + (abstand - loch_b) / 2
        for ly in (y + rand, y + hoehe - rand - loch_h):
            teile.append(f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{loch_b:.1f}" height="{loch_h:.1f}" '
                         f'rx="{loch_b * 0.25:.1f}" fill="{PERFO}"/>')
    return "".join(teile)


def filmstreifen(x, y, breite, hoehe, stufen, randschrift):
    """Streifen mit einem Bild je Eintrag in stufen (0 bis 4) und Randnummern wie bei Kleinbildfilm."""
    loch_h, loch_b, rand = hoehe * 0.075, hoehe * 0.05, hoehe * 0.06
    teile = [perforation(x, y, breite, hoehe, loch_b, loch_h, rand)]
    innen_y = y + rand * 2 + loch_h
    innen_h = hoehe - 2 * (rand * 2 + loch_h)
    luecke = breite * 0.0035
    bild_b = (breite - luecke * (len(stufen) + 1)) / len(stufen)
    for i, stufe in enumerate(stufen):
        bx = x + luecke + i * (bild_b + luecke)
        teile.append(f'<rect class="b s{stufe}" style="--i:{i}" x="{bx:.1f}" y="{innen_y:.1f}" '
                     f'width="{bild_b:.1f}" height="{innen_h:.1f}" rx="2"/>')
    for i in range(0, len(stufen), 6):
        bx = x + luecke + i * (bild_b + luecke)
        d, _ = pfad(randschrift, f"{i // 6 * 2 + 1}A", hoehe * 0.055, bx + 2, y + hoehe - rand * 0.25, sperr=0.06)
        teile.append(f'<path d="{d}" fill="{ORANGE}" opacity=".75"/>')
    return "".join(teile)
