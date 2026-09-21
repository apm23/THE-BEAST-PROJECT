# PLAY NOW LOOT V2

Status: **BUILT — awaiting normal gameplay smoke test**

Target: Dying Light: The Beast **1.71E**.

This replaces PLAY NOW LOOT V1 for the user's fast-play branch. Deeper per-item Ascension research remains separate.

## Requested gameplay flow

The V2 loot branch implements two conceptual stages:

1. enemy death/corpse loot rolls the **item category**;
2. if the selected category is melee weapon, firearm, or weapon-mod blueprint, a second weighted branch selects **rarity/tier**, then the final native item is generated.

For ordinary Biters the added target rates are:

- firearm: **~15%**;
- melee weapon: **~15%**;
- native weapon-mod blueprint: **~25%**;
- convenience `Ammo Blueprint Pack`: **~8%**.

Mapped stronger infected/human archetypes scale upward. Single-draw loot objects whose requested category probabilities cannot mathematically coexist are automatically scaled proportionally rather than invalidating/replacing vanilla loot.

## Rarity gacha

Conditional on an added melee/firearm/mod-blueprint category being selected:

- Green/T1: **10%**
- Rare/Blue/T2: **25%**
- Epic/Violet/T3: **35%**
- Legendary/Orange/T4: **30%**

This is not Orange recoloring. Melee Legendary uses native 1.71E definitions with Legendary-compatible affix groups; firearm rarity branches use native fixed-color firearm definitions. Mod blueprints use the 80 native `Craftplan_Mod_*` IDs split evenly into T1–T4 pools.

The generated weapon pools remain player-rank matched from rank 1 through 15.

## All-ammo crafting

Vanilla 1.71E already has craftplan IDs for arrows/bolts, flamethrower ammo, grenade-launcher variants, and sawblade ammo. V2 adds six missing standard firearm-ammo craftplans:

- Pistol
- SMG
- Rifle
- Shotgun
- Revolver
- Marksman

The custom recipes use existing native materials (`Craft_Firearm_Scrap_FT`, `Craft_Scrap`, and `Craft_Cleaning_Supplies`). A custom `DLTB_PlayNow_AllAmmoBlueprints` bundle grants the six V2 plans plus the 13 existing vanilla ammo plans; it is exposed as the `Ammo Blueprint Pack` in corpse loot so the user can unlock every ammo family without waiting for separate progression paths.

Custom output counts per craft are 15 pistol, 30 SMG, 20 rifle, 6 shotgun, 6 revolver, and 8 marksman ammo.

## Package

Local-only `data2.pak` SHA-256:

`92a649892c5b6ec750d7dc4b238e744e57f0e7183d7b741cff0bb54c4fdb8651`

Local user ZIP SHA-256:

`a813a4fe9e34f5ea29dcbda02c561bf6f53431f5175ee323927a423d8bd85069`

The binary PAK/ZIP is not committed to this public repository.

## Patched files inside local PAK

- `scripts/inventory/inventory_ranged.scr`
- `scripts/inventory/loot/lootsets_ft.loot`
- `scripts/inventory/loot/lootpools_ft.loot`

Static build gates passed: brace counts, expected PAK member list, ZIP integrity, rank-1-to-15 pool coverage, 20 blueprints per T1–T4 tier, and six custom + thirteen vanilla ammo-plan IDs in the all-ammo bundle.

## Safety / compatibility

- installer recognizes PLAY NOW V1 and known project POC hashes and can intentionally replace those;
- an unknown `data2.pak` is never overwritten;
- uninstaller deletes only the exact V2 hash;
- no vanilla source archive, save, EXE, DLL, or proprietary PAK is committed.

## Smoke test

After installing V2, first verify ordinary Biter corpses still have normal `F` interaction and ordinary loot. Over roughly 20–50 Biters verify that firearms are visibly less frequent than V1, melee/firearm/mod-blueprint drops show multiple rarity tiers including Orange over time, and the Ammo Blueprint Pack can be looted/redeemed. Then verify the Craft menu exposes standard firearm ammo recipes and at least one recipe crafts the expected ammo without inventory/save regression.
