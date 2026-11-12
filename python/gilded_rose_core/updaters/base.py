"""Base class that defines what happens to an item at the end of each day."""

from abc import ABC, abstractmethod

from gilded_rose_core.constants import MAX_QUALITY, MIN_QUALITY


class ItemUpdater(ABC):
    """Runs the same daily steps for every item; subclasses supply the rule.

    The steps are always:
      1. change the quality using today's rule,
      2. move ``sell_in`` one day closer,
      3. if the sell date has now passed, apply the expired rule.
    """

    def update(self, item):
        self._change_quality(item, self.quality_change(item))
        self.update_sell_in(item)
        if item.sell_in < 0:
            self.update_expired(item)

    @abstractmethod
    def quality_change(self, item):
        """How much quality changes today, based on the item before ``sell_in`` moves."""

    def update_sell_in(self, item):
        item.sell_in -= 1

    def update_expired(self, item):
        """Extra change once the sell date has passed. By default the daily rule repeats."""
        self._change_quality(item, self.quality_change(item))

    @staticmethod
    def _change_quality(item, amount):
        """Apply ``amount`` to quality without crossing the 0 and 50 limits.

        A value already outside the limits is left alone, exactly as the original
        code behaved.
        """
        if amount > 0 and item.quality < MAX_QUALITY:
            item.quality = min(MAX_QUALITY, item.quality + amount)
        elif amount < 0 and item.quality > MIN_QUALITY:
            item.quality = max(MIN_QUALITY, item.quality + amount)
