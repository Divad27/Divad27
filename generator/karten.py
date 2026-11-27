"""Karten für die öffentlichen Projekte, an denen David mitarbeitet. Jede verlinkt auf das Original-Repo."""
import json
from dataclasses import dataclass

from .schrift import pfad, saira, umbrechen
from .stil import perforation, svg

BREITE, HOEHE, BAND, RAND = 600, 300, 36, 36
TEXT_GROESSE, TEXT_ZEILEN = 32, 2


@dataclass(frozen=True)
class Beitrag:
    datei: str
    titel: str
    text: str
    link: str


def lade_liste(pfad_json):
    with open(pfad_json, encoding="utf-8") as f:
        return [Beitrag(**eintrag) for eintrag in json.load(f)]


def karte(beitrag, thema):
    innen = BREITE - 2 * RAND
    zeile = saira(400, 100)
    zeilen = umbrechen(zeile, beitrag.text, TEXT_GROESSE, innen)
    if len(zeilen) > TEXT_ZEILEN:
        raise ValueError(f"Text für {beitrag.titel!r} braucht {len(zeilen)} Zeilen, Platz ist für {TEXT_ZEILEN}")
    titel, _ = pfad(saira(900, 50), beitrag.titel, 100, RAND, 150, sperr=-0.015, max_breite=innen)
    teile = [
        f'<clipPath id="karte"><rect width="{BREITE}" height="{HOEHE}" rx="16"/></clipPath>',
        '<g clip-path="url(#karte)">',
        f'<rect width="{BREITE}" height="{HOEHE}" fill="{thema.grund}"/>',
        perforation(0, 0, BREITE, BAND, loch_b=12, loch_h=8, rand=5),
        f'<path d="{titel}" fill="{thema.text}"/>',
    ]
    for i, text in enumerate(zeilen):
        d, _ = pfad(zeile, text, TEXT_GROESSE, RAND, 206 + i * 42)
        teile.append(f'<path d="{d}" fill="{thema.leise}"/>')
    teile.append("</g>")
    return svg(BREITE, HOEHE, "".join(teile), f"{beitrag.titel}: {beitrag.text}")
