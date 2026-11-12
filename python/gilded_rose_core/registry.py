"""Decides which updater applies to an item."""

from gilded_rose_core.constants import AGED_BRIE, BACKSTAGE_PASS, SULFURAS
from gilded_rose_core.updaters.aged_brie import AgedBrieUpdater
from gilded_rose_core.updaters.backstage_pass import BackstagePassUpdater
from gilded_rose_core.updaters.normal import NormalUpdater
from gilded_rose_core.updaters.sulfuras import SulfurasUpdater

_DEFAULT = NormalUpdater()

_BY_NAME = {
    AGED_BRIE: AgedBrieUpdater(),
    BACKSTAGE_PASS: BackstagePassUpdater(),
    SULFURAS: SulfurasUpdater(),
}


def updater_for(item):
    """Return the updater for ``item``; anything unrecognised is a normal item."""
    return _BY_NAME.get(item.name, _DEFAULT)
