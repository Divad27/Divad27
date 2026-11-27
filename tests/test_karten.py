import xml.etree.ElementTree as ET

from generator.karten import Beitrag, karte, lade_liste, status
from generator.stil import DUNKEL, HELL

BEITRAG = Beitrag("zephyr", "Zephyr RTOS", "Board fixes for the Seeed XIAO nRF54LM20A",
                  "zephyrproject-rtos/zephyr", (114571, 114572), "https://example.org")
GEMERGT = {"state": "closed", "merged_at": "2026-01-01T00:00:00Z"}
OFFEN = {"state": "open", "merged_at": None}
ZU = {"state": "closed", "merged_at": None}


def test_status():
    assert status([GEMERGT, GEMERGT]) == ("2 MERGED", "gemergt")
    assert status([OFFEN]) == ("OPEN", "offen")
    assert status([GEMERGT, OFFEN]) == ("1 MERGED · 1 OPEN", "offen")
    assert status([ZU]) == ("CLOSED", "zu")


def test_karte_ist_gueltiges_svg():
    for thema in (HELL, DUNKEL):
        wurzel = ET.fromstring(karte(BEITRAG, "2 MERGED", "gemergt", thema))
        assert wurzel.get("aria-label") == "Zephyr RTOS: Board fixes for the Seeed XIAO nRF54LM20A"


def test_liste_aus_dem_repo():
    liste = lade_liste("beitraege.json")
    assert [b.datei for b in liste] == ["zephyr", "anyps5"]
    assert liste[0].prs == (114571, 114572)
