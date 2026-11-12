from gilded_rose_core.protocols import ItemLike
from gilded_rose_core.updaters.base import ItemUpdater


class AgedBrieUpdater(ItemUpdater):
    """Aged Brie gains 1 quality a day, and 2 a day once the sell date has passed."""

    def quality_change(self, item: ItemLike) -> int:
        return 1
