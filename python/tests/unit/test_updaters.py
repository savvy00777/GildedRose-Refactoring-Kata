import pytest

from gilded_rose import Item
from gilded_rose_core.updaters.aged_brie import AgedBrieUpdater
from gilded_rose_core.updaters.backstage_pass import BackstagePassUpdater
from gilded_rose_core.updaters.normal import NormalUpdater
from gilded_rose_core.updaters.sulfuras import SulfurasUpdater


def item(sell_in, quality):
    return Item("any", sell_in, quality)


def test_normal_loses_one():
    assert NormalUpdater().quality_change(item(5, 10)) == -1


def test_aged_brie_gains_one():
    assert AgedBrieUpdater().quality_change(item(5, 10)) == 1


@pytest.mark.parametrize(
    "sell_in, expected",
    [(20, 1), (11, 1), (10, 2), (6, 2), (5, 3), (1, 3), (0, 3)],
)
def test_backstage_pass_tiers(sell_in, expected):
    assert BackstagePassUpdater().quality_change(item(sell_in, 20)) == expected


def test_backstage_pass_is_worthless_after_the_concert():
    expired = item(-1, 35)
    BackstagePassUpdater().update_expired(expired)
    assert expired.quality == 0


def test_sulfuras_is_left_completely_alone():
    legendary = item(3, 80)
    SulfurasUpdater().update(legendary)
    assert (legendary.sell_in, legendary.quality) == (3, 80)
