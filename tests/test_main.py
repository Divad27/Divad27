from generator import __main__ as programm


def test_main_schreibt_alle_bilder(tmp_path, beitragsseite):
    quelle = tmp_path / "seite.html"
    quelle.write_text(beitragsseite([0, 3] * 185), encoding="utf-8")
    assert programm.main(["--aus", str(tmp_path / "out"), "--quelle", str(quelle)]) == 0
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == [
        "karte-anyps5-dunkel.svg", "karte-anyps5-hell.svg",
        "karte-noop-dunkel.svg", "karte-noop-hell.svg",
        "karte-zephyr-dunkel.svg", "karte-zephyr-hell.svg",
        "kopf-dunkel.svg", "kopf-hell.svg",
    ]


def test_main_bricht_bei_kaputten_daten_ab(tmp_path):
    quelle = tmp_path / "seite.html"
    quelle.write_text("<html></html>", encoding="utf-8")
    assert programm.main(["--aus", str(tmp_path / "out"), "--quelle", str(quelle)]) == 1
    assert not (tmp_path / "out").exists()
