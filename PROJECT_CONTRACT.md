# PROJECT CONTRACT

## Purpose

Build and maintain a mod for **Dying Light: The Beast VER. 1.71E** using the runtime-proven **USER HIGH LOOT SPECIAL45 / PROVEN45** loot lineage as the immutable foundation.

The current remake focuses on:

- preserving PROVEN45 global loot behavior;
- native weapon rarity rolls up to Exotic where supported;
- human corpse loot using zombie-style extra lootpool logic rather than held-weapon drops;
- special/high-tier infected loot;
- the project custom powerful outfit;
- expanded inventory and high stack limits through safe paths;
- Sense wallhack/QoL through isolated narrow overrides;
- one-sided CO-OP where the modded user can play with a vanilla sibling.

## Non-negotiable behavior

### PROVEN45 is the loot foundation

Do not replace the proven global loot root with a new override architecture.

Preserve the proven `LootedObject` / corpse-routing topology and corpse `F` interaction. Prefer numeric weight, quantity, and existing sub-pool edits over structural rewrites.

### Native rarity up to Exotic

Generated supported weapons may participate in a native rarity roll up to **Exotic** where DLTB 1.71E supports that quality/state.

Rarity must be real item state, not cosmetic text/color. Preserve weapon identity/model/class and keep RNG/farming.

### Human corpse loot, not held-weapon drops

The project does **not** target dropping the exact weapon visibly held by a human.

Human enemies should instead receive an extra searchable/corpse lootpool following the same design principle as infected loot while preserving the frozen PROVEN45 corpse route.

### Powerful outfit

Preserve/rebuild the project custom powerful outfit without introducing unsafe save/versioning rewrites.

### Inventory targets

Target capacities:

- Equipment `34`
- Consumable `34`
- Weapon `68`
- Ammo `42`

Target supported stack size: `99,999`.

Inventory changes must avoid previously unsafe inventory-versioning, stash-DLC, quickslot-topology, and save-versioning paths.

### Sense isolation

Sense/wallhack work must remain isolated from global loot, `LootedObject`, inventory versioning, save/versioning, controls/F, CP1, and item registry paths.

### One-sided CO-OP

Primary multiplayer target:

- modded user uses the gameplay mod;
- sibling remains vanilla and does not need to install the gameplay mod.

Use the runtime-proven data2-only / MultiMod lineage as the compatibility reference. The CO-OP-safe loader path may also stay active during single-player.

### Save and scene safety

Ordinary save reload, save-data swap, and scene transition must not silently restore vanilla behavior or break mod features.

New Game and NG+ remain separate validation targets until runtime-proven.

## Explicitly cancelled old goals

Do not reintroduce unless the user explicitly requests them again:

- Legendary Core;
- Rare/Epic -> Legendary Core conversion;
- Legendary Ascension;
- L+1..L+5 progression;
- Core drops/costs;
- human held-weapon drop feature;
- Manual Save Anywhere as part of this remake.

## Hard runtime gates

A candidate build is rejected if it breaks any of these:

1. save / DLC safety;
2. corpse loot interaction (`F`);
3. attack / ordinary controls;
4. runtime-proven PROVEN45 loot structure;
5. one-sided CO-OP compatibility after the feature reaches that test stage.

## Scope discipline

- Preserve runtime-proven structures.
- Make the smallest justified patch for each feature.
- Keep experimental features isolated so they can be rolled back independently.
- Distinguish STATIC-PROVEN, RUNTIME-PROVEN, UNTESTED, and REJECTED states.
- Do not silently alter unrelated game systems.

## Repository rules

Allowed in this public repository:

- project-authored configs
- patch descriptions/diffs
- scripts and validators
- workflow files
- documentation
- test records
- hashes/metadata for locally owned baseline files

Do not commit:

- original game archives
- extracted full vanilla data dumps
- save files
- account/user identifiers
- copyrighted game assets not authored by this project

## Continuation protocol

Before any new work:

1. Inspect actual GitHub HEAD.
2. Read `MASTER_STATE.md` completely.
3. Read this contract and `FEATURE_SPEC.md`.
4. Treat current user corrections as newer authority than stale historical goals in `MASTER_STATE.md`.
5. Inspect only the files/tests relevant to the next safe action.
6. Preserve frozen-green systems and documented failed hypotheses.
7. Perform the smallest justified next action.
8. Record meaningful state changes before expanding scope.
