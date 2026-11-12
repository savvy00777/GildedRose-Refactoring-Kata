from gilded_rose_core.updaters.base import ItemUpdater


class NormalUpdater(ItemUpdater):
    """Ordinary items lose 1 quality a day, and 2 a day once the sell date has passed."""

    def quality_change(self, item):
        return -1
