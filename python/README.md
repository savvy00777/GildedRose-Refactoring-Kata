# Gilded Rose starting position in Python

For exercise instructions see [top level README](../README.md)

Suggestion: create a python virtual environment for this project. See the [documentation](https://docs.python.org/3/library/venv.html)

## How this solution is organised

`gilded_rose.py` keeps the `Item` class (unchanged) and `GildedRose`. `update_quality()` no
longer holds any rules: it asks a registry for each item's updater and calls it.

```
gilded_rose.py                      Item (unchanged) + GildedRose
gilded_rose_core/
  constants.py                      quality limits, special item names, Conjured prefix
  protocols.py                      ItemLike: what an updater needs from an item
  registry.py                       updater_for(item): picks the updater
  updaters/
    base.py                         ItemUpdater: the same daily steps for every item
    normal.py  aged_brie.py  backstage_pass.py  sulfuras.py  conjured.py
tests/
  test_gilded_rose_approvals.py     golden master: 30 days of every item type
  unit/                             table-driven tests, property-based tests
```

Every item goes through the same daily steps in `ItemUpdater.update`: change the quality,
move `sell_in`, then apply the expired rule once the sell date has passed. An updater only
says how much quality changes (and overrides a step when its item is special). The 0 and 50
limits are applied in one place.

Assumption: an item is Conjured when its name starts with "Conjured".

### Add a new item type

1. Add `gilded_rose_core/updaters/<type>.py` with a subclass of `ItemUpdater` that returns
   the daily quality change from `quality_change`.
2. Register it in `gilded_rose_core/registry.py`: add its exact name to `_BY_NAME`, or add a
   name-prefix check next to the Conjured one in `updater_for`.
3. Add tests under `tests/unit/`.

### Run the checks

```
python -m pytest        # unit, property-based and golden-master tests
python -m mypy          # strict type check of gilded_rose_core
```

## Run the unit tests from the Command-Line

```
python -m pytest
```

## Run the TextTest fixture from the Command-Line

For e.g. 10 days:

```
python texttest_fixture.py 10
```

You should make sure the command shown above works when you execute it in a terminal before trying to use TextTest (see below).


## Run the TextTest approval test that comes with this project

There are instructions in the [TextTest Readme](../texttests/README.md) for setting up TextTest. You will need to specify the Python executable and interpreter in [config.gr](../texttests/config.gr). Uncomment these lines:

    executable:${TEXTTEST_HOME}/python/texttest_fixture.py
    interpreter:python

## Run the ApprovalTests.Python test

This test uses the framework [ApprovalTests.Python](https://github.com/approvals/ApprovalTests.Python). You will need to install  Run it like this:

```
python tests/test_gilded_rose_approvals.py
```

You will need to approve the output file which appears under "approved_files" by renaming it from xxx.received.txt to xxx.approved.txt.
