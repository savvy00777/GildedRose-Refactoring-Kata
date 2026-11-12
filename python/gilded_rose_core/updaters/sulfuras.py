from gilded_rose_core.protocols import ItemLike
from gilded_rose_core.updaters.base import ItemUpdater


class SulfurasUpdater(ItemUpdater):
    """Legendary item: never has to be sold and never loses quality."""

    def quality_change(self, item: ItemLike) -> int:
        return 0

    def update_sell_in(self, item: ItemLike) -> None:
        pass
