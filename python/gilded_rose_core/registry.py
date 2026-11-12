"""Decides which updater applies to an item."""

from gilded_rose_core.constants import (
    AGED_BRIE,
    BACKSTAGE_PASS,
    CONJURED_PREFIX,
    SULFURAS,
)
from gilded_rose_core.protocols import ItemLike
from gilded_rose_core.updaters.aged_brie import AgedBrieUpdater
from gilded_rose_core.updaters.backstage_pass import BackstagePassUpdater
from gilded_rose_core.updaters.base import ItemUpdater
from gilded_rose_core.updaters.conjured import ConjuredUpdater
from gilded_rose_core.updaters.normal import NormalUpdater
from gilded_rose_core.updaters.sulfuras import SulfurasUpdater

_DEFAULT: ItemUpdater = NormalUpdater()
_CONJURED: ItemUpdater = ConjuredUpdater()

_BY_NAME: dict[str, ItemUpdater] = {
    AGED_BRIE: AgedBrieUpdater(),
    BACKSTAGE_PASS: BackstagePassUpdater(),
    SULFURAS: SulfurasUpdater(),
}


def updater_for(item: ItemLike) -> ItemUpdater:
    """Return the updater for ``item``; anything unrecognised is a normal item."""
    if item.name in _BY_NAME:
        return _BY_NAME[item.name]
    if item.name.startswith(CONJURED_PREFIX):
        return _CONJURED
    return _DEFAULT
