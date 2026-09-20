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

**PHASE 1D — POC-001 is green; POC-002 persistent-upgrade probe is active. POC-002D is the current test artifact.**

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
- Vanilla `LootedObject("Biter")` has `LootAmount(2)` and a very large `Empty` path (`50.0` normal, `70.0` PermaWorld) before considering the other resource pools. `Biter_CommonResources` is only weight `20.0` normal / `23.0` PermaWorld. Therefore an item placed only inside `Biter_CommonResources` can still be impractical to obtain during a focused test even if its internal item weight is huge.
- `ShockMod_PowerAttack_FT_T4` is a native Orange/T4 Tip mod with native damage/durability effects and is suitable as a persistence probe.

## POC-001 — Native Legendary Opportunity/Camp Axe

Local-only artifact SHA-256:
`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

Confirmed runtime result:

- Camp Axe generated as **Legendary One-Handed Axe** from a vanilla Rare-path definition.
- Legendary identity, affixes, damage `131`, durability `160/160`, and repairs `7/7` survived save/reload and survived POC removal.
- Definition-added Tip/Shaft/Grip sockets did **not** survive uninstall; only vanilla Charm Socket remained.

Frozen conclusion: rarity/affixes/damage/durability/repair count can persist per item strongly enough to survive mod removal; definition-only socket structure cannot be assumed persistent.

## POC-002 — Persistent per-item upgrade probe

Goal: install a native Shock T4 modification on the existing Legendary Camp Axe and determine separately whether mod UI/socket, damage bonus, and durability bonus persist across save/reload and uninstall.

### Rejected iteration: POC-002 initial

A custom Biter loot subroutine removed corpse `F` loot interaction. Rejected.

### Rejected iteration: POC-002B

Intended Shock injection landed in `Resin_FT` because the builder used an ambiguous global `Craft_Resin` anchor. User killed 100+ zombies without Shock. Rejected builder strategy.

### Rejected as a test-delivery strategy: POC-002C

- Shock was correctly injected inside existing `Biter_CommonResources`.
- Vanilla Biter outer loot structure remained intact.
- Runtime looting worked, but user reported **many `Nothing` results** and Shock remained impractical to obtain for the persistence test.
- Cause is now understood: the outer Biter pool still strongly favors `Empty` and other branches. A huge Shock weight inside `Biter_CommonResources` does nothing on rolls where that sub-pool is not selected.
- This is not evidence that Shock itself is invalid; it is a bad test-delivery strategy.

### Current iteration: POC-002D — deterministic test delivery

Local-only `data2.pak` SHA-256:
`9dca23d8adf0155eb22d859f1f799f03fedaa61787d5e0f4d4624b3cc60b8020`

POC-002D is intentionally **not final balance**. It exists only to stop wasting test time:

- starts from vanilla 1.71E Biter loot definitions;
- preserves Biter `LootAmount(2)`;
- keeps the existing Biter loot architecture, with no custom subroutine;
- injects Shock T4 only inside the real `Biter_CommonResources` block;
- gives Shock internal weight `1,000,000`;
- changes the existing `Biter_CommonResources` calls in Biter/Biter_Permadeath test paths to weight `1,000,000` and `min_amount=1`;
- retains the POC-002 Camp Axe socket/effect test changes;
- installer safely recognizes and replaces known POC-002 / 002B / 002C hashes.

Expected test behavior: one or a few ordinary Biters should be enough to obtain Shock T4. If not, stop killing zombies and inspect the exact runtime loot-object path instead of increasing weights again.

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

## Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** confirmed NOT persistent.

## Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine: rejected after corpse loot interaction disappeared.
2. POC-002B global first-match resource-anchor patching: rejected; wrong subroutine was modified.
3. POC-002C inner-weight-only delivery: rejected for focused testing because outer vanilla Biter loot RNG still produced too many `Nothing` outcomes.

## next_safe_action

**Run POC-002D on the TEST SAVE.**

1. Close game and install POC-002D; installer may replace POC-002/002B/002C directly when their known hash is present.
2. Kill and loot one or a few ordinary Biters.
3. If Shock T4 does not appear quickly, stop and inspect the runtime loot-object path; do not farm hundreds more.
4. Before installing Shock, record Camp Axe damage/durability and Poison/Freeze state.
5. Install Shock T4 into the Tip socket and record changed stats.
6. Save, quit, reload with POC-002D installed and re-check.
7. If reload is green, uninstall POC-002D and reload the same save.
8. Record separately whether Shock UI/socket, damage bonus, and durability bonus persist.

Do not proceed to full Ascension/Core/global gacha until this persistence result is known.