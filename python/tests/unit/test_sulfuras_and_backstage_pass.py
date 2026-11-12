import pytest

from helpers import BACKSTAGE_PASS, SULFURAS, update_one_day


@pytest.mark.parametrize("sell_in", [5, 0, -1])
def test_sulfuras_never_changes(sell_in):
    assert update_one_day(SULFURAS, sell_in, 80) == (sell_in, 80)


@pytest.mark.parametrize(
    "sell_in, quality, expected",
    [
        pytest.param(11, 20, (10, 21), id="+1 with more than 10 days left"),
        pytest.param(10, 20, (9, 22), id="+2 at 10 days"),
        pytest.param(6, 20, (5, 22), id="+2 at 6 days"),
        pytest.param(5, 20, (4, 23), id="+3 at 5 days"),
        pytest.param(1, 20, (0, 23), id="+3 on the last day before the concert"),
        pytest.param(0, 20, (-1, 0), id="drops to 0 after the concert"),
        pytest.param(-1, 20, (-2, 0), id="stays 0 long after the concert"),
        pytest.param(11, 50, (10, 50), id="capped at 50 with +1"),
        pytest.param(10, 49, (9, 50), id="capped at 50 with +2"),
        pytest.param(5, 49, (4, 50), id="capped at 50 with +3"),
        pytest.param(5, 48, (4, 50), id="+3 reaching exactly the cap"),
    ],
)
def test_backstage_pass(sell_in, quality, expected):
    assert update_one_day(BACKSTAGE_PASS, sell_in, quality) == expected
