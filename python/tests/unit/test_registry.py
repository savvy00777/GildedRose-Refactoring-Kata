import pytest

from gilded_rose import Item
from gilded_rose_core.registry import updater_for
from gilded_rose_core.updaters.aged_brie import AgedBrieUpdater
from gilded_rose_core.updaters.backstage_pass import BackstagePassUpdater
from gilded_rose_core.updaters.normal import NormalUpdater
from gilded_rose_core.updaters.sulfuras import SulfurasUpdater

from helpers import AGED_BRIE, BACKSTAGE_PASS, NORMAL, SULFURAS


@pytest.mark.parametrize(
    "name, expected",
    [
        pytest.param(AGED_BRIE, AgedBrieUpdater, id="Aged Brie"),
        pytest.param(BACKSTAGE_PASS, BackstagePassUpdater, id="Backstage pass"),
        pytest.param(SULFURAS, SulfurasUpdater, id="Sulfuras"),
        pytest.param(NORMAL, NormalUpdater, id="ordinary item"),
        pytest.param("Something nobody has heard of", NormalUpdater, id="unknown item is normal"),
    ],
)
def test_picks_the_right_updater(name, expected):
    assert isinstance(updater_for(Item(name, 5, 10)), expected)
