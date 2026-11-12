import pytest

from gilded_rose import Item
from gilded_rose_core.updaters.base import ItemUpdater


class FixedChange(ItemUpdater):
    """Tiny updater used to test the shared daily steps in isolation."""

    def __init__(self, amount):
        self.amount = amount

    def quality_change(self, item):
        return self.amount


def run(amount, sell_in, quality):
    item = Item("any", sell_in, quality)
    FixedChange(amount).update(item)
    return item.sell_in, item.quality


def test_cannot_be_used_without_a_rule():
    with pytest.raises(TypeError):
        ItemUpdater()


@pytest.mark.parametrize(
    "amount, sell_in, quality, expected",
    [
        pytest.param(-1, 5, 10, (4, 9), id="applies the change once before the sell date"),
        pytest.param(-1, 0, 10, (-1, 8), id="applies the change twice once expired"),
        pytest.param(2, 5, 10, (4, 12), id="increase is applied"),
        pytest.param(2, 5, 49, (4, 50), id="increase stops at 50"),
        pytest.param(-2, 5, 1, (4, 0), id="decrease stops at 0"),
        pytest.param(1, 5, 60, (4, 60), id="value above 50 is left alone on increase"),
        pytest.param(-1, 5, -3, (4, -3), id="value below 0 is left alone on decrease"),
        pytest.param(0, 0, 10, (-1, 10), id="zero change leaves quality alone"),
    ],
)
def test_daily_steps(amount, sell_in, quality, expected):
    assert run(amount, sell_in, quality) == expected
