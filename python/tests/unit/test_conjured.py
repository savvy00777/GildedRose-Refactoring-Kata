import pytest

from gilded_rose import Item
from gilded_rose_core.registry import updater_for

from helpers import update_one_day

CONJURED = "Conjured Mana Cake"


@pytest.mark.parametrize(
    "sell_in, quality, expected",
    [
        pytest.param(5, 20, (4, 18), id="loses 2 a day, twice as fast as a normal item"),
        pytest.param(1, 20, (0, 18), id="still loses 2 on the last day"),
        pytest.param(0, 20, (-1, 16), id="loses 4 once the sell date has passed"),
        pytest.param(-1, 10, (-2, 6), id="keeps losing 4 when expired"),
        pytest.param(5, 50, (4, 48), id="starts from the maximum quality"),
        pytest.param(5, 1, (4, 0), id="never below 0 with 1 left"),
        pytest.param(0, 3, (-1, 0), id="expired item floors at 0"),
        pytest.param(0, 1, (-1, 0), id="expired item with 1 left floors at 0"),
        pytest.param(5, 0, (4, 0), id="already at 0 stays at 0"),
    ],
)
def test_conjured_item(sell_in, quality, expected):
    assert update_one_day(CONJURED, sell_in, quality) == expected


@pytest.mark.parametrize(
    "name, expected_daily_change",
    [
        pytest.param("Conjured Mana Cake", -2, id="name starting with Conjured"),
        pytest.param("Conjured Elixir of the Mongoose", -2, id="any Conjured item"),
        pytest.param("Unconjured Cloak", -1, id="Conjured only counts at the start"),
        pytest.param("Mana Cake", -1, id="no Conjured prefix is a normal item"),
    ],
)
def test_registry_recognises_conjured_by_name(name, expected_daily_change):
    item = Item(name, 5, 20)
    assert updater_for(item).quality_change(item) == expected_daily_change
