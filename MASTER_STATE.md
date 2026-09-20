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

**PHASE 1D — POC-001 is green; POC-002 persistent-upgrade probe is active. A manual native Venom/Poison install test is now the current runtime path.**

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

### POC-002E — generated Camp Axe with native StartupMod

Local-only `data2.pak` SHA-256:
`76cac0e401c0ca21f7639b71f957680d6a19fb53cb8089c51531f1610d840191`

POC-002E avoids loose weapon-mod loot entirely:

- reuses the already-proven POC-001 deterministic Camp Axe weapon-lottery path;
- keeps the test Camp Axe native Legendary with Legendary affix groups and four test sockets while installed;
- adds native `StartupMod("ShockMod_Random_FT_T4_TIP")` to a newly generated test Camp Axe;
- uses a vanilla-supported weapon-generation mechanism rather than trying to materialize a CraftPart directly from corpse resources.

POC-002E remains a valid fallback, but it is no longer required for the current persistence test because the user already owns native Poison/Venom and Freeze mods and can install them manually into the exposed test sockets.

### Current runtime probe — manual Venom/Poison install

User provided before/after screenshots for the same Legendary Camp Axe while the four test sockets were exposed.

**Before installing Venom/Poison:**

- rarity: **Legendary One-Handed Axe**;
- damage: **131 Slashing Damage / 131 Base Damage**;
- affixes: `+33% Damage (Melee Weapon Throw)`, `+6% Damage (Infected)`, `-7.5% Stamina Cost (Melee Weapons)`;
- durability: **160/160**;
- repairs remaining: **7/7**;
- Tip, Shaft, Grip, and Charm sockets visible and empty.

**Immediately after installing the user's Poison mod into Tip Socket:**

- visible installed mod/effect: **Venom — Applies TOXIC on critical hits**;
- damage: **137 Slashing Damage / 137 Base Damage**;
- durability: **185/185**;
- repairs remaining: **7/7** unchanged;
- Legendary rarity and the three rolled affixes unchanged;
- Shaft, Grip, and Charm sockets remain empty.

Observed immediate deltas from the installed Poison/Venom mod:

- damage: **131 -> 137** (`+6`, approximately `+4.58%` displayed base damage);
- durability: **160 -> 185** (`+25`, `+15.625%`);
- repairs: unchanged at **7/7**.

This is the clean baseline for the persistence test. The relevant question is now whether the installed Venom state and/or its `+6` damage and `+25` durability survive save/reload and then survive removal of the mod package that exposes Tip/Shaft/Grip.

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

**Complete the manual Venom persistence test on the TEST SAVE.**

1. With the Poison/Venom mod already installed in the Camp Axe Tip Socket, save and exit normally.
2. Relaunch with the current POC/mod package still installed and inspect the same axe.
3. PASS for reload stage if Venom is still installed and the weapon still shows **137 damage, 185/185 durability, 7/7 repairs**, unchanged Legendary rarity, and unchanged rolled affixes.
4. If reload stage is green, close the game and uninstall the current POC/mod package.
5. Relaunch vanilla 1.71E and inspect the exact same axe.
6. Record separately whether:
   - Venom UI/state remains visible;
   - damage remains `137` or falls back to `131`;
   - durability remains `185/185` or falls back to `160/160`;
   - Tip/Shaft/Grip socket structure disappears as expected from POC-001;
   - Legendary rarity, rolled affixes, and repairs remain intact.
7. Do not proceed to full Ascension/Core/global gacha until this uninstall persistence result is known.
