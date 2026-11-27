import xml.etree.ElementTree as ET

import pytest

from generator.karten import Beitrag, karte, lade_liste
from generator.stil import DUNKEL, HELL

BEITRAG = Beitrag("zephyr", "Zephyr RTOS", "Real-time OS for small embedded devices", "https://example.org")


def test_karte_ist_gueltiges_svg():
    for thema in (HELL, DUNKEL):
        wurzel = ET.fromstring(karte(BEITRAG, thema))
        assert wurzel.get("aria-label") == "Zephyr RTOS: Real-time OS for small embedded devices"


def test_zu_langer_text_wird_abgelehnt():
    with pytest.raises(ValueError):
        karte(Beitrag("x", "X", "word " * 60, "https://example.org"), HELL)


def test_liste_aus_dem_repo():
    liste = lade_liste("beitraege.json")
    assert [b.datei for b in liste] == ["zephyr", "anyps5", "noop"]
    assert all(b.link.startswith("https://github.com/") for b in liste)
    for b in liste:
        karte(b, HELL)
