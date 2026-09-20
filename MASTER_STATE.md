# MASTER_STATE

## Authority

This file plus actual GitHub HEAD are authoritative for continuation. Reconcile both before acting.

## Baseline

- Game: **Dying Light: The Beast**
- Target build: **VER. 1.71E**
- Fresh-install baseline captured before mod development.
- Clean save remains local/private and must not be committed.
- Clean archive map: `data0.pak,data1.pak`.
- Targeted 1.71E extraction completed locally: **58 requested files, 0 missing**.

## Current phase

**PHASE 1D — POC-001 is green; POC-002 persistent-upgrade probe is active. POC-002E is the current test artifact.**

Global gacha, Legendary Core, full Ascension, and Manual Save Anywhere are not implemented yet.

## Frozen project goals

1. Universal native Legendary eligibility even for weapons vanilla-capped at Rare/Epic.
2. Global per-weapon rarity gacha; initial Legendary target ~30% per generated weapon.
3. Slightly increased weapon availability from common infected, humans, and supported loot sources.
4. Human held weapon itself participates in rarity gacha.
5. Legendary must be real item quality/state, not cosmetic recolor.
6. Legendary Core: Rare/Epic -> Legendary, Legendary -> per-item Ascension.
7. Ascension: L -> L+1 -> L+2 -> L+3 -> L+4 -> L+5.
8. Ascension emphasizes damage/durability; secondary stats moderate; attack speed conservative.
9. Per-weapon progression, not a global definition-only buff where persistent item state is possible.
10. Preserve weapon identity/model/class.
11. Keep RNG/farming in the final mod.
12. Manual Save Anywhere: hotkey-driven native save request from ordinary gameplay locations, blocked only during unsafe transient/loading/death states.

## Initial balance targets

- Legendary per generated weapon: **30%**.
- Common Biter weapon availability: **20–25%** final target, subject to loot semantics/inventory pressure.
- Human held-weapon drop: preserve confirmed vanilla `LootChance(1.0)` where present; extra corpse weapon lottery tuned separately.
- Legendary Core target chances: common infected 8–10%, Viral/human ~10%, special infected 12–15%, ordinary containers 8–10%, good/locked chest 12–15%, boss/Chimera 20–30%.
- Core costs: Rare/Epic->Legendary 1; L->L+1 1; +1->+2 2; +2->+3 3; +3->+4 5; +4->+5 8.

## Confirmed 1.71E mapping

See `docs/BASELINE_1.71E_MAPPING.md`.

- Blue = Rare; Violet = Epic; Orange = Legendary; Platinum/Exotic exist above Orange.
- Key files include `inventory_gen.scr`, `itemaffixes.scr`, `lootpools_ft.loot`, `lootsets_ft.loot`, `weaponprobpresets.scr`, `weaponscolorpresets.scr`, `weaponsetpresets.scr`, `weaponenhancmentcosts.scr`, and `crafting_effects.scr`.
- Native Legendary generation uses class-specific Legendary affix groups plus `Weapons_Random_Legendary_ft`.
- Lower-rarity weapons can hardcode Rare affix groups; Universal Legendary cannot be cosmetic-only.
- Standard inspected human weapon presets use held-weapon `LootChance(1.0)`.
- Vanilla `LootedObject("Biter")` has `LootAmount(2)` and a very large `Empty` path (`50.0` normal, `70.0` PermaWorld) before considering the other resource pools. `Biter_CommonResources` is only weight `20.0` normal / `23.0` PermaWorld.
- `ShockMod_PowerAttack_FT_T4` and `ShockMod_Random_FT_T4_TIP` are native Orange/T4 weapon mods. Their definitions are `CategoryType_CraftPart` / `ItemType_CraftPart` with native damage/durability effects.
- In the targeted vanilla loot mappings inspected for this project, direct `Item(...)` loot entries are used for many inventory categories, but no normal corpse-loot precedent for directly materializing `CategoryType_CraftPart` weapon mods was found. Treat direct loose-mod injection into Biter resource loot as unsupported until separately proven.
- `StartupMod(...)` is a confirmed native generation mechanism: vanilla generated weapons use visible T4 mods such as `HeatMod_Random_FT_T4_TIP` and invisible built-in mods on special weapons.

## POC-001 — Native Legendary Opportunity/Camp Axe

Local-only artifact SHA-256:
`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

Confirmed runtime result:

- Camp Axe generated as **Legendary One-Handed Axe** from a vanilla Rare-path definition.
- Legendary identity, affixes, damage `131`, durability `160/160`, and repairs `7/7` survived save/reload and survived POC removal.
- Definition-added Tip/Shaft/Grip sockets did **not** survive uninstall; only vanilla Charm Socket remained.

Frozen conclusion: rarity/affixes/damage/durability/repair count can persist per item strongly enough to survive mod removal; definition-only socket structure cannot be assumed persistent.

## POC-002 — Persistent per-item upgrade probe

Goal: determine separately whether a native installed weapon mod, its damage bonus, and its durability bonus persist across save/reload and uninstall.

### Rejected iteration: POC-002 initial

A custom Biter loot subroutine removed corpse `F` loot interaction. Rejected.

### Rejected iteration: POC-002B

Intended Shock injection landed in `Resin_FT` because the builder used an ambiguous global `Craft_Resin` anchor. User killed 100+ zombies without Shock. Rejected builder strategy.

### Rejected iteration: POC-002C

Shock was correctly injected inside existing `Biter_CommonResources`, but vanilla outer Biter loot still strongly favored `Empty`; many `Nothing` results made it impractical for focused testing.

### Rejected iteration: POC-002D

POC-002D forced the outer Biter resource path and removed the practical `Empty` problem. Runtime result:

- user reported Biter loot was no longer empty;
- despite this, **Shock T4 still never materialized**;
- therefore the outer loot-object patch was active, but direct loose `CategoryType_CraftPart` delivery through this corpse resource set did not produce the mod item in runtime.

Conclusion: stop increasing weights. The loose-Shock-via-Biter strategy is rejected. This is a delivery-path failure, not evidence that native Shock mods or their crafting effects are invalid.

### Current iteration: POC-002E — generated Camp Axe with native StartupMod

Local-only `data2.pak` SHA-256:
`76cac0e401c0ca21f7639b71f957680d6a19fb53cb8089c51531f1610d840191`

POC-002E avoids loose weapon-mod loot entirely:

- reuses the already-proven POC-001 deterministic Camp Axe weapon-lottery path;
- keeps the test Camp Axe native Legendary with Legendary affix groups and four test sockets while installed;
- adds native `StartupMod("ShockMod_Random_FT_T4_TIP")` to the newly generated test Camp Axe;
- uses a vanilla-supported weapon-generation mechanism rather than trying to materialize a CraftPart directly from corpse resources;
- keeps the old Camp Axe untouched; the persistence target is a **new Camp Axe generated while POC-002E is installed**;
- installer recognizes and safely replaces known POC-001 / POC-002 / 002B / 002C / 002D hashes.

Expected test: obtain a new Legendary Camp Axe with Shock T4 already installed, record stats, save/reload with POC present, then uninstall and inspect whether Shock UI/state and its damage/durability effects remain.

## Manual Save Anywhere

Feature is frozen in `FEATURE_SPEC.md`, but implementation is pending native save-trigger mapping.

Collector V2 failed before extraction due a PowerShell path parsing bug. Collector V3 was built to enumerate archive paths first and broadly collect save/checkpoint/input/state/invoke candidates. No claim of a working F5 save exists yet.

## Technical invariants

- Do not commit proprietary PAKs, vanilla extracted archives, saves, or local-only binary test artifacts.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists merely because it survives reload while the mod remains installed.
- Treat definition-only sockets/structure as runtime-dependent unless separately proven persistent.
- Keep held-weapon drop and extra corpse-loot weapon rolls separate.
- Attack speed remains safety-sensitive.
- Scope loot-builder edits to exact named sub/object blocks; do not use ambiguous global first-match anchors.
- Test-delivery builds may be deterministic; final game balance must return to the frozen RNG targets.
- Do not keep tuning loot weights after a runtime result proves the targeted delivery mechanism itself is not materializing the intended item class.

## Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** confirmed NOT persistent.

## Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine: rejected after corpse loot interaction disappeared.
2. POC-002B global first-match resource-anchor patching: rejected; wrong subroutine was modified.
3. POC-002C inner-weight-only delivery: rejected for focused testing because outer vanilla Biter RNG still produced too many `Nothing` outcomes.
4. POC-002D direct loose Shock CraftPart through forced `Biter_CommonResources`: rejected after runtime showed non-empty loot but still no Shock item.

## next_safe_action

**Run POC-002E on the TEST SAVE.**

1. Close the game and install POC-002E; installer may replace known older POC builds directly.
2. Keep the old Camp Axe; the test target is a **new** Camp Axe generated after POC-002E installation.
3. Kill/loot ordinary Biters until the new Legendary Camp Axe drops using the same proven POC-001 weapon-lottery path.
4. Open Modify on the new axe and confirm Shock T4 is already installed via StartupMod.
5. Record weapon damage, durability, rarity/affixes, visible mod state, and sockets.
6. Save, quit, reload with POC-002E installed and re-check the same axe.
7. If reload is green, close the game, uninstall POC-002E, reopen vanilla, and inspect the same axe.
8. Record separately whether Shock mod UI/state, damage bonus, durability bonus, rarity and affixes persist.

Do not proceed to full Ascension/Core/global gacha until this persistence result is known.