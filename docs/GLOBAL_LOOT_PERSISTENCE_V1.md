# GLOBAL LOOT PERSISTENCE V1 — EXPERIMENTAL

Status: **STATIC-PROVEN / RUNTIME UNTESTED**

Canonical proven baseline remains **USER HIGH LOOT SPECIAL45** (`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`). This experiment does **not** replace SPECIAL45 as the project baseline until the runtime matrix passes.

## Problem statement

Observed runtime behavior indicates that custom loot can appear correct in one state and later look vanilla after changing scene/level or changing/replacing saves. The project goal is that loot **rules** are global mod definitions and that saves only retain world/player state and already-created item results.

Required behavior:

- mod installed -> Save A -> custom loot
- mod installed -> Save B -> custom loot
- replace save -> custom loot
- New Game -> custom loot
- NG+ -> custom loot

No save file should need a manual loot-table edit.

## Static findings from current repository + 1.71E baseline

1. The canonical SPECIAL45 payload contains only:
   - `scripts/inventory/inventory_ranged.scr`
   - `scripts/inventory/loot/lootpools_ft.loot`
   - `scripts/inventory/loot/lootsets_ft.loot`
2. The project installer copies gameplay PAKs and backs up saves. There is no committed project code that writes SPECIAL45 loot rules into a save.
3. Vanilla `scripts/inventory/loot/default.loot` is the root loot definition and imports `lootpools_ft.loot`.
4. `lootpools_ft.loot` imports `lootsets_ft.loot`.
5. `default()`, `default_hard()`, and `default_nightmare()` all call `Loot_FT()`.
6. Current SPECIAL45 overrides the child files but does **not** override `default.loot` itself.

Therefore, the hypothesis that THE-BEAST-PROJECT intentionally stores loot definitions inside one save is **not supported by the current source**.

Two remaining runtime explanations are plausible:

- the engine rebuilds/rebinds the loot root on save/scene load and can resolve the vanilla child graph instead of the modded child graph; or
- the save/world stores already-generated loot instances, so old entities/containers can legitimately retain vanilla-generated results even while the global rules are still modded.

V1 tests the first explanation with the smallest possible architecture change.

## V1 architecture: mod-owned root binding

Instead of relying on vanilla `default.loot` to import a generic filename that the overlay system must resolve, data2 owns the root graph:

`data2.pak`

- `scripts/inventory/inventory_ranged.scr` — byte-identical SPECIAL45
- `scripts/inventory/loot/default.loot` — vanilla 1.71E root with **one import binding changed**
- `scripts/inventory/loot/tbp_lootpools_global_v1.loot` — byte-identical SPECIAL45 pool content except **one import binding changed**
- `scripts/inventory/loot/tbp_lootsets_global_v1.loot` — byte-identical SPECIAL45 lootset content

Binding:

`default.loot -> tbp_lootpools_global_v1.loot -> tbp_lootsets_global_v1.loot`

The root remains the same for Normal / Hard / Nightmare because all three vanilla root functions still call `Loot_FT()`.

## What V1 deliberately does NOT change

- no `LootedObject` body is rewritten;
- no corpse route is added, removed, or reordered;
- no rarity weights are changed;
- no resource amounts are changed;
- no inventory/versioning/save code is touched;
- no `player_variables` change;
- no co-op/CP1 change;
- no item registry deletion/reorder;
- no save file patching.

This is a binding/persistence experiment only.

## Deterministic build contract

Builder:

`tools/build_special45_global_loot_root_v1.py`

Input SPECIAL45 SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

1.71E `default.loot` SHA-256:

`757e2f7a606eae5dce5b2f7d045b5184bc32daabcf52a5cd369bed682476e88f`

Expected GLOBAL ROOT V1 data2 SHA-256:

`32c129265ef9f9e2eb889946f91cff7119316e110c34180bc0d4cbbe60a54b7b`

The builder reverse-verifies both import edits so no other source content changes silently.

## Runtime Definition of Done

Use a disposable or fully backed-up test state.

1. Install GLOBAL ROOT V1.
2. Load Save A and test newly spawned infected / newly generated loot.
3. Exit game completely.
4. Replace with a previously vanilla Save B.
5. Load Save B and test newly spawned infected / newly generated loot.
6. Exit game completely.
7. Create New Game and test newly spawned loot.
8. If available, test NG+ or another save slot.
9. At each step verify:
   - corpse `F` works;
   - custom weapon rarity/loot behavior matches SPECIAL45;
   - resource behavior matches SPECIAL45;
   - no DLC-disabled warning;
   - data2 remains exact GLOBAL ROOT V1 hash.

V1 is promoted only if custom loot remains active across the full matrix.

## If V1 fails

Do **not** increase resource amounts again and do **not** rewrite `LootedObject`.

The next investigation should target whether individual world entities/containers serialize already-generated loot. That requires a read-only comparison of freshly spawned entities versus persisted entities and, if needed, a narrow generation/on-spawn hook. A save-edit workaround is explicitly rejected.

## Scope note: Legendary Core / Ascension

MASTER_STATE still marks the final Legendary Core and true uninstall-persistent Ascension L+1..L+5 as **not implemented**. GLOBAL ROOT V1 is the persistence substrate for loot definitions; it does not pretend those unfinished systems already exist. Once a system is implemented as a mod definition, it should enter through the same global root architecture instead of being embedded into one save.
