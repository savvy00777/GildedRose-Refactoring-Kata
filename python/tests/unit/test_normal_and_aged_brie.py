import pytest

from helpers import AGED_BRIE, NORMAL, update_one_day


@pytest.mark.parametrize(
    "sell_in, quality, expected",
    [
        pytest.param(10, 20, (9, 19), id="degrades by 1 before sell date"),
        pytest.param(1, 20, (0, 19), id="still 1 on the last day"),
        pytest.param(0, 20, (-1, 18), id="degrades by 2 once sell date passed"),
        pytest.param(-1, 10, (-2, 8), id="keeps degrading by 2 when expired"),
        pytest.param(5, 0, (4, 0), id="never below 0"),
        pytest.param(0, 1, (-1, 0), id="expired item floors at 0"),
        pytest.param(0, 0, (-1, 0), id="expired item at 0 stays 0"),
    ],
)
def test_normal_item(sell_in, quality, expected):
    assert update_one_day(NORMAL, sell_in, quality) == expected


@pytest.mark.parametrize(
    "sell_in, quality, expected",
    [
        pytest.param(5, 10, (4, 11), id="improves by 1 before sell date"),
        pytest.param(0, 10, (-1, 12), id="improves by 2 once sell date passed"),
        pytest.param(-1, 20, (-2, 22), id="keeps improving by 2 when expired"),
        pytest.param(5, 50, (4, 50), id="capped at 50"),
        pytest.param(0, 49, (-1, 50), id="double improvement still capped at 50"),
        pytest.param(0, 50, (-1, 50), id="expired item stays at 50"),
    ],
)
def test_aged_brie(sell_in, quality, expected):
    assert update_one_day(AGED_BRIE, sell_in, quality) == expected
