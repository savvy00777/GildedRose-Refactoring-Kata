"""Property-based tests: rules that must hold for *any* valid item, not just chosen examples."""

from hypothesis import given, settings
from hypothesis import strategies as st

from helpers import AGED_BRIE, BACKSTAGE_PASS, NORMAL, SULFURAS, update_one_day

CONJURED = "Conjured Mana Cake"

NON_LEGENDARY = st.sampled_from([NORMAL, AGED_BRIE, BACKSTAGE_PASS, CONJURED])
SELL_IN = st.integers(min_value=-50, max_value=50)
QUALITY = st.integers(min_value=0, max_value=50)

many_examples = settings(max_examples=300, deadline=None)


@many_examples
@given(name=NON_LEGENDARY, sell_in=SELL_IN, quality=QUALITY)
def test_quality_stays_between_0_and_50(name, sell_in, quality):
    _, new_quality = update_one_day(name, sell_in, quality)
    assert 0 <= new_quality <= 50


@many_examples
@given(name=NON_LEGENDARY, sell_in=SELL_IN, quality=QUALITY)
def test_sell_in_drops_by_one_a_day(name, sell_in, quality):
    new_sell_in, _ = update_one_day(name, sell_in, quality)
    assert new_sell_in == sell_in - 1


@many_examples
@given(sell_in=SELL_IN)
def test_sulfuras_never_changes(sell_in):
    assert update_one_day(SULFURAS, sell_in, 80) == (sell_in, 80)


@many_examples
@given(sell_in=SELL_IN, quality=QUALITY)
def test_aged_brie_never_loses_quality(sell_in, quality):
    _, new_quality = update_one_day(AGED_BRIE, sell_in, quality)
    assert new_quality >= quality


@many_examples
@given(sell_in=st.integers(min_value=1, max_value=50), quality=QUALITY)
def test_backstage_pass_never_loses_quality_before_the_concert(sell_in, quality):
    _, new_quality = update_one_day(BACKSTAGE_PASS, sell_in, quality)
    assert new_quality >= quality


@many_examples
@given(sell_in=st.integers(min_value=-50, max_value=0), quality=QUALITY)
def test_backstage_pass_is_worthless_after_the_concert(sell_in, quality):
    _, new_quality = update_one_day(BACKSTAGE_PASS, sell_in, quality)
    assert new_quality == 0


@many_examples
@given(sell_in=SELL_IN, quality=QUALITY)
def test_conjured_loses_exactly_twice_what_a_normal_item_loses(sell_in, quality):
    _, conjured = update_one_day(CONJURED, sell_in, quality)
    _, normal = update_one_day(NORMAL, sell_in, quality)
    normal_loss = quality - normal
    assert conjured == max(0, quality - 2 * normal_loss)


@many_examples
@given(
    name=NON_LEGENDARY,
    sell_in=SELL_IN,
    quality=QUALITY,
    days=st.integers(min_value=1, max_value=60),
)
def test_quality_stays_in_range_over_many_days(name, sell_in, quality, days):
    for _ in range(days):
        sell_in, quality = update_one_day(name, sell_in, quality)
        assert 0 <= quality <= 50
