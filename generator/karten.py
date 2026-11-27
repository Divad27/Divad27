"""Karten für Beiträge zu fremden Projekten, Status live aus der REST-API."""
import json
import urllib.request
from dataclasses import dataclass

from .schrift import pfad, saira
from .stil import ORANGE, perforation, svg

BREITE, HOEHE, BAND = 800, 250, 40


@dataclass(frozen=True)
class Beitrag:
    datei: str
    titel: str
    text: str
    repo: str
    prs: tuple
    link: str


def lade_liste(pfad_json):
    with open(pfad_json, encoding="utf-8") as f:
        return [Beitrag(**{**eintrag, "prs": tuple(eintrag["prs"])}) for eintrag in json.load(f)]


def hole_pr(repo, nummer, token=None):
    kopf = {"Accept": "application/vnd.github+json", "User-Agent": "github-profile-readme"}
    if token:
        kopf["Authorization"] = f"Bearer {token}"
    anfrage = urllib.request.Request(f"https://api.github.com/repos/{repo}/pulls/{nummer}", headers=kopf)
    with urllib.request.urlopen(anfrage, timeout=20) as antwort:
        return json.load(antwort)


def status(antworten):
    """(Beschriftung, Art) aus den PR-Antworten. Art ist offen, gemergt oder zu."""
    gemergt = sum(1 for a in antworten if a.get("merged_at"))
    offen = sum(1 for a in antworten if a["state"] == "open")
    zu = len(antworten) - gemergt - offen
    mehrere = len(antworten) > 1
    teile = [f"{n} {wort}" if mehrere else wort
             for n, wort in ((gemergt, "MERGED"), (offen, "OPEN"), (zu, "CLOSED")) if n]
    art = "offen" if offen else "gemergt" if gemergt else "zu"
    return " · ".join(teile), art


def karte(beitrag, beschriftung, art, thema):
    farbe = {"offen": ORANGE, "gemergt": thema.akzent, "zu": thema.leise}[art]
    marke, _ = pfad(saira(600, 75), beschriftung, 24, 40, 86, sperr=0.04)
    titel, _ = pfad(saira(900, 50), beitrag.titel, 100, 40, 170, sperr=-0.015, max_breite=BREITE - 80)
    text, _ = pfad(saira(400, 100), beitrag.text, 30, 40, 220, max_breite=BREITE - 80)
    teile = [
        f'<clipPath id="karte"><rect width="{BREITE}" height="{HOEHE}" rx="16"/></clipPath>',
        '<g clip-path="url(#karte)">',
        f'<rect width="{BREITE}" height="{HOEHE}" fill="{thema.grund}"/>',
        perforation(0, 0, BREITE, BAND, loch_b=12, loch_h=8, rand=6),
        f'<path d="{marke}" fill="{farbe}"/>',
        f'<path d="{titel}" fill="{thema.text}"/>',
        f'<path d="{text}" fill="{thema.leise}"/>',
        "</g>",
    ]
    return svg(BREITE, HOEHE, "".join(teile), f"{beitrag.titel}: {beitrag.text}")
