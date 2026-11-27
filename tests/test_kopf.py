import xml.etree.ElementTree as ET

from generator.kopf import _mehrzahl, kopf
from generator.stil import DUNKEL, HELL

NS = "{http://www.w3.org/2000/svg}"


def test_kopf_hat_52_bilder():
    for thema in (HELL, DUNKEL):
        wurzel = ET.fromstring(kopf([i % 5 for i in range(52)], 1190, 127, thema))
        bilder = [r for r in wurzel.iter(f"{NS}rect") if r.get("class", "").startswith("b ")]
        assert len(bilder) == 52
        assert wurzel.get("aria-label") == "Daxidfoto – Photos from the trail, code from the desk."


def test_mehrzahl():
    assert _mehrzahl(1, "DAY") == "1 DAY"
    assert _mehrzahl(1190, "CONTRIBUTION") == "1,190 CONTRIBUTIONS"
