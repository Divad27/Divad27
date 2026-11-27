"""Alle Profilbilder erzeugen:  python -m generator --aus out [--quelle beitragsseite.html]"""
import argparse
import os
import sys
from pathlib import Path

from . import daten, karten
from .kopf import kopf
from .stil import THEMEN

WURZEL = Path(__file__).resolve().parent.parent


def main(argv=None):
    parser = argparse.ArgumentParser(description="Profilbilder erzeugen")
    parser.add_argument("--aus", required=True, help="Zielordner")
    parser.add_argument("--quelle", help="gespeicherte Beitragsseite statt Abruf (für Tests)")
    argumente = parser.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN")
    try:
        seite = Path(argumente.quelle).read_text(encoding="utf-8") if argumente.quelle else daten.hole()
        tage = daten.lese(seite)
        beitraege = karten.lade_liste(WURZEL / "beitraege.json")
        stati = {b.datei: karten.status([karten.hole_pr(b.repo, n, token) for n in b.prs]) for b in beitraege}
    except (OSError, ValueError, KeyError) as fehler:
        print(f"generator: {fehler}", file=sys.stderr)
        return 1
    stufen = daten.stufen(daten.wochen(tage))
    summe, aktiv = daten.jahr(tage)
    ziel = Path(argumente.aus)
    ziel.mkdir(parents=True, exist_ok=True)
    for thema in THEMEN:
        (ziel / f"kopf-{thema.name}.svg").write_text(kopf(stufen, summe, aktiv, thema), encoding="utf-8")
        for b in beitraege:
            beschriftung, art = stati[b.datei]
            (ziel / f"karte-{b.datei}-{thema.name}.svg").write_text(
                karten.karte(b, beschriftung, art, thema), encoding="utf-8")
    print(f"{summe} contributions on {aktiv} days, {len(beitraege)} cards -> {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
