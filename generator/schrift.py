"""Text als SVG-Pfad. GitHub zeigt SVGs als <img>, da lädt kein Webfont."""
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SAIRA = Path(__file__).resolve().parent.parent / "fonts" / "saira-latin-standard-normal.woff2"


@lru_cache(maxsize=None)
def saira(wght, wdth):
    return instantiateVariableFont(TTFont(SAIRA), {"wght": wght, "wdth": wdth})


def _zahl(wert):
    return f"{wert:.1f}".rstrip("0").rstrip(".")


def pfad(font, inhalt, groesse, x, y, sperr=0.0, anker="start", max_breite=None):
    """Pfad-d für inhalt mit Grundlinie bei y, sperr in em. Ist der Text breiter als max_breite,
    wird er kleiner gesetzt. Gibt (d, breite) zurück."""
    cmap, glyphen, hmtx = font.getBestCmap(), font.getGlyphSet(), font["hmtx"]
    try:
        namen = [cmap[ord(z)] for z in inhalt]
    except KeyError as fehler:
        raise ValueError(f"Zeichen fehlt in der Schrift: {inhalt!r}") from fehler
    upm = font["head"].unitsPerEm

    def breite_bei(g):
        return sum(hmtx[n][0] for n in namen) * g / upm + sperr * g * (len(namen) - 1)

    if max_breite and breite_bei(groesse) > max_breite:
        groesse *= max_breite / breite_bei(groesse)
    breite = breite_bei(groesse)
    if anker == "end":
        x -= breite
    elif anker == "middle":
        x -= breite / 2
    stift = SVGPathPen(glyphen, ntos=_zahl)
    s = groesse / upm
    for n in namen:
        glyphen[n].draw(TransformPen(stift, (s, 0, 0, -s, x, y)))
        x += hmtx[n][0] * s + sperr * groesse
    return stift.getCommands(), breite


def umbrechen(font, inhalt, groesse, max_breite):
    """Teilt inhalt an Leerzeichen in Zeilen, die höchstens max_breite breit sind."""
    zeilen = []
    for wort in inhalt.split():
        probe = f"{zeilen[-1]} {wort}" if zeilen else wort
        if zeilen and pfad(font, probe, groesse, 0, 0)[1] <= max_breite:
            zeilen[-1] = probe
        else:
            zeilen.append(wort)
    return zeilen
