from gilded_rose import GildedRose, Item

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
NORMAL = "+5 Dexterity Vest"


def update_one_day(name, sell_in, quality):
    """Run a single daily update on one item and return (sell_in, quality)."""
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item.sell_in, item.quality
