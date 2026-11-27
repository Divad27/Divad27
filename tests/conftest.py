import datetime as dt

import pytest


def _seite(anzahlen, start=dt.date(2025, 11, 22)):
    """Nachbau der GitHub-Beitragsseite: je Tag eine Zelle und ein Tooltip."""
    teile = []
    for i, n in enumerate(anzahlen):
        tag = start + dt.timedelta(days=i)
        stufe = 0 if n == 0 else min(4, 1 + n // 5)
        text = "No contributions on X." if n == 0 else f"{n:,} contribution{'' if n == 1 else 's'} on X."
        teile.append(f'<td data-date="{tag}" data-level="{stufe}" id="z{i}"></td><tool-tip for="z{i}">{text}</tool-tip>')
    return "<table><tr>" + "".join(teile) + "</tr></table>"


@pytest.fixture
def beitragsseite():
    return _seite
