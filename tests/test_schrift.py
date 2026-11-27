import pytest

from generator.schrift import pfad, saira, umbrechen


def test_umbrechen_haelt_max_breite_ein():
    font = saira(400, 100)
    satz = "Offline WHOOP companion that keeps all data on your device"
    zeilen = umbrechen(font, satz, 32, 300)
    assert len(zeilen) > 1
    assert " ".join(zeilen) == satz
    assert all(pfad(font, z, 32, 0, 0)[1] <= 300 for z in zeilen)


def test_pfad_liefert_kontur_und_breite():
    d, breite = pfad(saira(900, 50), "Daxidfoto", 100, 0, 100)
    assert d.startswith("M")
    assert breite > 100


def test_max_breite_setzt_kleiner():
    _, breite = pfad(saira(400, 100), "a fairly long line of text", 50, 0, 50, max_breite=100)
    assert breite == pytest.approx(100)


def test_sperrung_macht_breiter():
    font = saira(600, 75)
    _, eng = pfad(font, "MERGED", 24, 0, 24)
    _, weit = pfad(font, "MERGED", 24, 0, 24, sperr=0.04)
    assert weit == pytest.approx(eng + 0.04 * 24 * 5)


def test_fehlendes_zeichen():
    with pytest.raises(ValueError):
        pfad(saira(400, 100), "\u2603", 20, 0, 20)
