import pytest
from _lnlpcli import LNLPCLI


def test_logging():
    cli = LNLPCLI(debug=True)
    assert set(cli.global_session.logs["info"]) == set(
        [
            "Initialized Global Session Object and Global Driver",
        ]
    )
