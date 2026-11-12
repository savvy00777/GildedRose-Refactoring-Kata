from gilded_rose_core.constants import MIN_QUALITY
from gilded_rose_core.updaters.base import ItemUpdater


class BackstagePassUpdater(ItemUpdater):
    """Passes gain more quality as the concert approaches, then become worthless."""

    def quality_change(self, item):
        if item.sell_in <= 5:
            return 3
        if item.sell_in <= 10:
            return 2
        return 1

    def update_expired(self, item):
        item.quality = MIN_QUALITY
