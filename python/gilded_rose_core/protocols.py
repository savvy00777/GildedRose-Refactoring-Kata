"""What the updaters need from an item.

``Item`` itself cannot be changed, so the updaters depend on this small
description of it instead of on the class.
"""

from typing import Protocol


class ItemLike(Protocol):
    name: str
    sell_in: int
    quality: int
