# FEATURE SPECIFICATION — REMAKE ON PROVEN45

## Authority

This file defines the current remake target. The canonical USER HIGH LOOT SPECIAL45 / PROVEN45 loot lineage is the immutable gameplay foundation.

Do not redesign or structurally replace the proven global loot root. New features must be layered around the proven topology and must preserve corpse `F`, DLC/save safety, scene/save persistence, and one-sided CO-OP behavior.

## 1. Global loot foundation — PROVEN45 only

Use the existing runtime-proven USER HIGH LOOT SPECIAL45 implementation as the global loot foundation.

Rules:

- preserve the proven `LootedObject` / corpse routing topology;
- do not introduce a new global-root override architecture;
- prefer numeric weights, existing sub-pool contents, and safe quantity edits over structural rewrites;
- preserve the known-good SPECIAL45 resource balance and ammo/blueprint behavior unless explicitly changed later;
- any file that would alter the frozen corpse route requires separate proof before inclusion.

## 2. Weapon rarity system — up to Exotic

Supported generated weapons may roll through the game's native rarity/quality ladder up to **Exotic** where the 1.71E engine and item definition support it.

Requirements:

- rarity must be the real native item quality/state, not cosmetic text/color;
- preserve weapon identity/model/class;
- keep RNG/farming rather than guaranteeing the highest rarity;
- do not add Legendary Core or Ascension systems;
- do not add L+1..L+5 progression.

Exact rarity weights remain tuning values until runtime testing.

## 3. Human corpse lootpool — zombie-style extra loot, not held-weapon drop

Humans receive a corpse/search lootpool following the same design principle as infected corpse loot.

This feature is explicitly **not** a system that drops the weapon visibly held by the human.

Requirements:

- use a separate corpse-loot roll compatible with the frozen PROVEN45 routing;
- generated weapon loot uses the same rarity system up to Exotic;
- resource/material quantities should follow proven balance unless explicitly tuned later;
- do not replace or depend on held-weapon `LootChance(...)` behavior.

## 4. Exotic / special infected drops

Special infected and supported high-tier enemy sources may have stronger access to high-tier weapon rolls, including Exotic where natively supported.

Do not fabricate new item identities solely to simulate Exotic. Prefer native quality/affix mechanisms.

## 5. Custom powerful outfit

Preserve/rebuild the project custom powerful outfit feature.

Requirements:

- use a safe existing/native item identity where practical for one-sided CO-OP compatibility;
- avoid save/versioning rewrites;
- keep the outfit independent from the frozen PROVEN45 corpse topology;
- verify equip, unequip, save/reload, scene transition, and one-sided CO-OP behavior.

Exact bonuses are a tuning surface and must be documented in the build manifest used for testing.

## 6. Expanded inventory

Target capacities:

- Equipment: `34`
- Consumable: `34`
- Weapon: `68`
- Ammo: `42`

The implementation must avoid inventory-versioning, save-versioning, stash-DLC, quickslot topology, and other previously unsafe paths.

Inventory expansion is not considered runtime-proven until it survives:

1. initial load;
2. scene transition;
3. save reload;
4. save swap;
5. one-sided CO-OP session.

## 7. Huge stack size

Target stack size for supported materials / consumables / throwables: `99,999` where the underlying item/category safely permits it.

Do not force this onto categories whose native semantics make large stacking unsafe.

## 8. Dismantle compatibility

Supported modded/generated items should retain normal dismantle behavior where the base game provides it.

## 9. Drop / share compatibility

Supported items should remain droppable/shareable where the base game allows it. One-sided CO-OP tests must verify that a vanilla sibling can coexist with the modded player without requiring the sibling to install the gameplay mod.

## 10. Sense wallhack

Target Sense behavior:

- infected + humans visible through walls;
- effective range around `200 m`;
- highlight duration around `15 s`;
- dormant relevant AI detectable;
- dead AI skipped.

Sense must remain isolated from global loot, `LootedObject`, inventory versioning, save/versioning, controls/F, CP1, and item registry paths.

Previously rejected broad Sense V4/V4.1-style edits remain blacklisted. Prefer the narrow/effective-source approach.

## 11. One-sided CO-OP support

Primary compatibility target:

- modded user: full gameplay mod;
- sibling/client: vanilla, no gameplay mod required.

The proven architectural reference is the `CP1_COOP_SAFE_DATA2_ONLY` / MultiMod data2-only lineage.

The CO-OP-safe loader path may remain active in single-player; it is a load topology, not a separate gameplay ruleset.

## 12. Save / scene persistence

Features must remain active and correct after:

- ordinary save reload;
- save-data swap;
- scene transition;
- single-player to CO-OP usage through the proven loader path.

New Game / NG+ remain separate validation targets until explicitly runtime-tested.

## 13. Corpse F compatibility

Corpse search interaction using `F` is a hard gate. If `F` disappears or corpse routing breaks, the candidate build is rejected regardless of other improvements.

## 14. Attack / controls compatibility

Attack and ordinary control input must remain normal. Gameplay input regressions reject the candidate build.

## 15. Installer / rollback discipline

Every experimental build must provide:

- explicit clean/install path;
- status/detection where practical;
- rollback to the last runtime-proven state;
- clear distinction between STATIC-PROVEN, RUNTIME-PROVEN, and UNTESTED/HYPOTHESIS.

## Explicitly removed from the project target

The following old goals are cancelled unless the user explicitly reopens them later:

- Legendary Core;
- Rare/Epic -> Legendary Core upgrade path;
- Legendary Ascension;
- L+1..L+5 progression;
- Core drop chances/costs;
- human held-weapon drop as a project feature;
- Manual Save Anywhere as part of this remake.
