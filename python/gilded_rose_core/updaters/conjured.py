from gilded_rose_core.protocols import ItemLike
from gilded_rose_core.updaters.base import ItemUpdater


class ConjuredUpdater(ItemUpdater):
    """Conjured items lose 2 quality a day, and 4 a day once the sell date has passed."""

    def quality_change(self, item: ItemLike) -> int:
        return -2
