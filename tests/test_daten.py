import datetime as dt

import pytest

from generator import daten


def test_lese_liest_alle_tage(beitragsseite):
    tage = daten.lese(beitragsseite([0] * 300 + [3] * 70))
    assert len(tage) == 370
    assert sum(t[1] for t in tage) == 210


def test_lese_versteht_tausender(beitragsseite):
    assert daten.lese(beitragsseite([0] * 369 + [1204]))[-1][1] == 1204


def test_lese_lehnt_doppelten_tag_ab(beitragsseite):
    seite = beitragsseite([1] * 370).replace('data-date="2026-01-10"', 'data-date="2026-01-09"')
    with pytest.raises(ValueError):
        daten.lese(seite)


def test_lese_lehnt_zu_wenige_tage_ab(beitragsseite):
    with pytest.raises(ValueError):
        daten.lese(beitragsseite([1] * 100))


def test_wochen_beginnen_montags():
    montag = dt.date(2025, 11, 24)
    assert montag.weekday() == 0
    tage = [[str(montag + dt.timedelta(days=i)), 1, 1] for i in range(14)]
    assert daten.wochen(tage, anzahl=2) == [7, 7]


def test_wochen_nimmt_nur_die_letzten():
    montag = dt.date(2025, 11, 24)
    tage = [[str(montag + dt.timedelta(days=i)), i // 7, 1] for i in range(21)]
    assert daten.wochen(tage, anzahl=2) == [7, 14]


def test_stufen_nach_quartilen():
    assert daten.stufen([0, 1, 2, 3, 4, 5, 6, 7, 8]) == [0, 1, 1, 1, 2, 2, 3, 3, 4]


def test_stufen_ohne_beitraege():
    assert daten.stufen([0, 0, 0]) == [0, 0, 0]


def test_jahr_zaehlt_die_letzten_365_tage():
    start = dt.date(2025, 11, 22)
    tage = [[str(start + dt.timedelta(days=i)), 2 if i % 2 else 0, 1 if i % 2 else 0] for i in range(370)]
    aktiv = sum(1 for i in range(5, 370) if i % 2)
    assert daten.jahr(tage) == (2 * aktiv, aktiv)
