"""Alle Profilbilder erzeugen:  python -m generator --aus out [--quelle beitragsseite.html]"""
import argparse
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
    try:
        seite = Path(argumente.quelle).read_text(encoding="utf-8") if argumente.quelle else daten.hole()
        tage = daten.lese(seite)
        beitraege = karten.lade_liste(WURZEL / "beitraege.json")
        stufen = daten.stufen(daten.wochen(tage))
        summe, aktiv = daten.jahr(tage)
        bilder = {}
        for thema in THEMEN:
            bilder[f"kopf-{thema.name}.svg"] = kopf(stufen, summe, aktiv, thema)
            for b in beitraege:
                bilder[f"karte-{b.datei}-{thema.name}.svg"] = karten.karte(b, thema)
    except (OSError, ValueError, KeyError, TypeError) as fehler:
        print(f"generator: {fehler}", file=sys.stderr)
        return 1
    ziel = Path(argumente.aus)
    ziel.mkdir(parents=True, exist_ok=True)
    for name, inhalt in bilder.items():
        (ziel / name).write_text(inhalt, encoding="utf-8")
    print(f"{summe} contributions on {aktiv} days, {len(beitraege)} cards -> {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
