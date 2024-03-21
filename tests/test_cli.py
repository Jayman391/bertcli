import pytest
from src._nllpcli import NLLPCLI


def test_logging():
    cli = NLLPCLI(debug=True)
    assert set(cli.global_session.logs["info"]) == set(
        [
            "Initialized Global Session Object and Global Driver",
        ]
    )
