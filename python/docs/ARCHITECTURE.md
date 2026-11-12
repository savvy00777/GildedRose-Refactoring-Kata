# Gilded Rose: Architecture Proposal

## Summary
Replace the nested conditional in `update_quality()` with one small, isolated rule per item
type. This lets us add **Conjured** items now, and future item types later, without touching
existing logic. Delivery is incremental and guarded by tests, and existing behaviour is not
changed.

## Problem
- All pricing rules live in one deeply nested `if` block.
- Each new item type means editing it and risking regressions in the others.
- The next requirement, Conjured items, makes this worse.

## Constraints
- `Item` and the `items` list are owned by another team and cannot change.
- Existing behaviour must be preserved exactly.

## Proposed design
One updater per item category, chosen by a registry.

| Component | Responsibility |
|---|---|
| `GildedRose` | Public entry point, unchanged. Loops over items and delegates. |
| `ItemUpdater` (base) | Runs the same daily sequence for every item: change quality, move `sell_in`, apply any after-sell-date change. Clamps quality to 0-50 in one place. |
| Updaters | Normal, Aged Brie, Backstage Pass, Sulfuras, Conjured. Each holds only its own rule. |
| Registry | Maps an item to its updater by exact name or name prefix. |

## Why this design
| Option | Assessment |
|---|---|
| Add a Conjured branch to the existing `if`s | Smallest change, but complexity keeps compounding |
| **Updater classes + registry** | Rules are isolated and independently testable; a new type is one new file |
| Declarative rules table | Less code, but awkward for tiered rules such as Backstage passes |
| Dynamic plugin loading | Over-engineered for this scope |

## Assumptions
- An item is Conjured if its name starts with "Conjured".
- Combinations such as "Conjured Aged Brie" are out of scope.
- Quality never goes below 0 or above 50, except Sulfuras, which is fixed at 80.

## Adding a new item type
1. Add one updater file.
2. Register its name or prefix.
3. Add its unit tests.

## Risk and rollout
- A golden-master test (30 days, every item type) proves the refactor changes nothing.
- Work ships as small, reviewable PRs: tests first, then the refactor, then Conjured.
- The golden master changes only in the Conjured PR, in its own commit with the reason stated.

## Future considerations
Configuration-driven item types, update metrics, and performance at larger scale.
