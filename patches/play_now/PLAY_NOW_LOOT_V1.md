# PLAY NOW LOOT V1

Status: **BUILT — awaiting normal gameplay smoke test**

Target: Dying Light: The Beast **1.71E**.

This is a fast playable loot-expansion branch requested by the user while deeper Ascension research remains separate. It does **not** modify or claim to solve L+1/L+2 progression.

## Scope

Adds two new corpse-loot categories using native 1.71E item IDs:

1. random firearm, rank-matched to player level 1–15;
2. random native weapon-mod blueprint.

The firearm pool contains 20 verified droppable/shareable vanilla firearm families across ranks 1–15, including pistol, SMG, rifle/marksman, shotgun, grenade launcher, flamethrower, and sawblade launcher variants. NPC-only firearm definitions and bows/crossbows are excluded.

The blueprint pool contains **80** native `Craftplan_Mod_*` item IDs recovered from the 1.71E inventory versioning tables: Bleeding, Freeze, Heat, Impact, Shock, Toxic, Damage, and Reinforce families across their available T1–T4/slot/trigger variants.

## Requested chance targets

The mod uses the vanilla weighted corpse-loot system. The added weights are solved against each normal loot object's existing weight sum and `LootAmount`, so the values below are per-category approximate targets, not guaranteed streak protection:

- Biter: ~25% firearm + ~25% mod blueprint
- Biter Police / Viral: ~30% + ~30%
- lighter special infected: ~35% + ~35%
- Charger/Goon/Demolisher/Corruptor/Bolter: ~40% + ~40%
- Volatile / Volatile Apex / Tyrant: ~45% + ~45%
- ordinary human archetypes: ~35% + ~35%
- firearm human archetypes: ~40% + ~40%
- mapped bosses: ~45% + ~45%

The same additions are also injected into mapped `PermaWorld()` branches where present.

## Patched enemy loot objects

27 mapped loot objects are touched, including Biter, Biter_Police, Viral, Screamer, Spitter, Banshee, Hag, Suicider, Charger, Goon, Demolisher, Corruptor, Bolter, Volatile, Volatile_Apex, Tyrant, common human archetypes, firearm human archetypes, `Human_Boss_Lieutenant`, and `Baron_Boss_Rifleman_Loot`.

## Package

Local-only `data2.pak` SHA-256:

`76865f2c42bbf1f5d4a9ebb0512ce65435cf908dea91b4076397911f3f01939a`

Local user ZIP SHA-256:

`7ea5f0c5d2d828576d2eacb37bf833e62deedd7376382500b6405c8655a49ace`

The binary PAK is not committed to this public repository.

## Safety

- package contains only patched `scripts/inventory/loot/lootsets_ft.loot` and `scripts/inventory/loot/lootpools_ft.loot`;
- installer refuses to overwrite an unknown `data2.pak`;
- uninstaller removes only the exact PLAY NOW LOOT V1 hash;
- known older THE BEAST PROJECT weapon POC hashes can be replaced intentionally by the installer;
- no save, proprietary game archive, EXE, or DLL is committed.

## Smoke test

Install, load a disposable/current gameplay save, kill ordinary Biters first, and verify:

- corpse interaction remains available;
- ordinary loot still appears;
- firearms can appear without replacing every corpse drop;
- `Craftplan_Mod_*` blueprints can appear;
- stronger enemy classes show visibly more frequent added drops over time;
- no inventory/save corruption occurs.

Do not infer exact percentages from a tiny sample; this build prioritizes playability and fast feedback.