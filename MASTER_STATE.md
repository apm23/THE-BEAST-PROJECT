# MASTER_STATE

## Authority

This file plus actual GitHub HEAD are authoritative for continuation. Reconcile both before acting.

## Baseline

- Game: **Dying Light: The Beast**
- Target build: **VER. 1.71E**
- Fresh install baseline; no mods installed originally.
- Clean test save captured locally as `save_ft_0.sav`; do not commit saves.
- Clean archive map: `data0.pak,data1.pak`.
- Targeted 1.71E extraction completed locally: **58 requested files, 0 missing**.

## Current phase

**PHASE 1D — POC-001 is green; POC-002 persistent-upgrade probe is active. POC-002C awaits runtime test.**

Global gacha, Legendary Core, Ascension, and Manual Save Anywhere are not implemented yet.

## Frozen project goals

1. Universal native Legendary eligibility even for weapons vanilla-capped at Rare/Epic.
2. Global per-weapon rarity gacha; initial Legendary target ~30% per generated weapon.
3. Slightly increased weapon availability from common infected, humans, and supported loot sources.
4. Human held weapon itself participates in rarity gacha.
5. Legendary must be real item quality/state, not cosmetic recolor.
6. Legendary Core: Rare/Epic -> Legendary, Legendary -> per-item Ascension.
7. Ascension: L -> L+1 -> L+2 -> L+3 -> L+4 -> L+5.
8. Ascension emphasizes damage and durability; secondary stats moderate; attack speed conservative.
9. Per-weapon progression, not a global definition-only buff where persistent item state is possible.
10. Preserve weapon identity/model/class.
11. Keep RNG/farming.
12. Manual Save Anywhere: hotkey-driven native save request from ordinary gameplay locations, blocked only during unsafe transient/loading/death states.

## Initial balance targets

- Legendary per generated weapon: **30%**.
- Common Biter weapon availability: **20–25%** target, subject to loot semantics/inventory pressure.
- Human held-weapon drop: preserve confirmed vanilla `LootChance(1.0)` where present; extra corpse weapon lottery tuned separately.
- Legendary Core drop targets:
  - common infected: 8–10%
  - Viral/human: ~10%
  - special infected: 12–15%
  - ordinary containers: 8–10%
  - good/locked chest: 12–15%
  - boss/Chimera: 20–30%
- Core costs: Rare/Epic->Legendary 1; L->L+1 1; +1->+2 2; +2->+3 3; +3->+4 5; +4->+5 8.

## Confirmed 1.71E mapping

See `docs/BASELINE_1.71E_MAPPING.md`.

- Blue = Rare; Violet = Epic; Orange = Legendary; Platinum/Exotic exist above Orange.
- Key files include:
  - `scripts/inventory/inventory_weapondefintions_ft.scr`
  - `scripts/inventory/inventory_gen.scr`
  - `scripts/inventory/itemaffixes.scr`
  - `scripts/inventory/loot/color_sets.loot`
  - `scripts/inventory/loot/lootpools_ft.loot`
  - `scripts/inventory/loot/lootsets_ft.loot`
  - `scripts/inventory/loot/weaponprobpresets.scr`
  - `scripts/inventory/loot/weaponscolorpresets.scr`
  - `scripts/inventory/loot/weaponsetpresets.scr`
  - `scripts/inventory/weaponenhancmentcosts.scr`
  - `scripts/crafting/crafting_effects.scr`
- Generated weapon rank instances expose stable UID/rank/tier/damage-tier linkage and forced/random affix-group names.
- Native Legendary generation uses class-specific Legendary affix groups plus `Weapons_Random_Legendary_ft`.
- Lower-rarity generated weapons can hardcode Rare affix groups; Universal Legendary cannot be cosmetic-only.
- Standard inspected human weapon presets use held-weapon `LootChance(1.0)`.
- Biter/Viral corpse pools already contain a tiny Orange-only `Enemy_Lottery_Weapons` path; human corpse pools also have a separate tiny Orange-only lottery.
- Vanilla `LootedObject("Biter")` uses `LootAmount(2)` and includes `Biter_CommonResources` with weight `20.0` in the normal branch and `23.0` in the PermaWorld branch.
- `crafting_effects.scr` exposes native damage/durability/swing-speed effects potentially reusable for Ascension.
- `ShockMod_PowerAttack_FT_T4` is a native Orange/T4 Tip mod with native increased-damage and increased-durability crafting effects and is suitable as a persistence probe.

## POC-001 — Native Legendary Opportunity/Camp Axe

Documentation: `patches/poc/POC_001_NATIVE_LEGENDARY.md`.

Local-only test artifact SHA-256:
`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

### Runtime results — confirmed

**With POC installed:**

- Game boot/load: PASS.
- Biter loot produced **Camp Axe — Legendary One-Handed Axe**.
- Orange/Legendary identity: PASS.
- Legendary-style affixes: PASS.
- Durability/repair values observed **160/160** and **7/7**.
- Modify screen exposed **Tip, Shaft, Grip, Charm** sockets while the POC definition was present.
- Save -> quit -> reload with POC still installed: PASS.

**After uninstalling POC and loading the same save:**

- Legendary identity remained: PASS persistent.
- Damage `131` remained: PASS persistent.
- Legendary affixes remained: PASS persistent.
- Durability `160/160` remained: PASS persistent.
- Repairs `7/7` remained: PASS persistent.
- Extra Tip/Shaft/Grip sockets disappeared; only vanilla Charm Socket remained.

### Persistence conclusion

Rarity/Legendary identity, rolled affixes, damage, durability, and repair count can persist strongly enough to survive mod removal. Definition-added socket availability does not persist by this method.

## POC-002 — Persistent per-item upgrade probe

Documentation: `patches/poc/POC_002_PERSISTENT_UPGRADE.md`.

Goal: use a native weapon mod/effect on the existing persistent Legendary Camp Axe and determine separately whether the mod/socket UI, damage bonus, and durability bonus persist across save/reload and uninstall.

### Failed iteration: POC-002 initial

- Added a custom `POC002_AscensionTestMod` subroutine to Biter loot.
- Runtime result: dead Biters lost the `F` loot interaction.
- This delivery method is rejected.

### Failed iteration: POC-002B

- Restored vanilla Biter outer loot structure and `LootAmount` so corpses became lootable again.
- Intended to inject Shock T4 into `Biter_CommonResources`.
- User killed **100+ zombies** without receiving Shock.
- Post-build audit found the exact reason: builder used a global first-match `Craft_Resin` anchor, so Shock was inserted into `Resin_FT`, not `Biter_CommonResources`.
- Therefore this is a patch-builder targeting failure, not evidence that high loot weight failed.

### Current iteration: POC-002C

Local-only `data2.pak` SHA-256:
`5eea00f64c213b469ce250e08a24285d92aa00f942c99fe2784df7e057bb18fb`

POC-002C:

- starts from vanilla 1.71E `lootpools_ft.loot` and `lootsets_ft.loot`;
- keeps vanilla Biter `LootAmount` and outer loot-pool structure unchanged;
- adds no custom loot subroutine;
- injects `ShockMod_PowerAttack_FT_T4` only inside the existing `Biter_CommonResources` block;
- uses temporary internal weight `1000.0` to shorten testing;
- retains the POC-002 inventory/inventory-gen changes needed for the Camp Axe socket/effect test;
- installer recognizes and safely replaces known POC-002 / POC-002B `data2.pak` hashes.

Static validation confirmed the Shock entry occurs exactly once and inside `Biter_CommonResources`.

## Manual Save Anywhere

Feature is frozen in `FEATURE_SPEC.md`, but implementation is pending native save-trigger mapping.

Collector V2 failed due a PowerShell path parsing bug before extracting useful data. Collector V3 was built to enumerate archive paths first and broadly collect save/checkpoint/input/state/invoke candidates. No claim of a working F5 save exists yet.

## Technical invariants

- Do not commit original PAKs, vanilla extracted archives, save files, or local-only binary test artifacts.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists just because it survives a reload with the mod installed.
- Treat definition-only sockets/structure as runtime-dependent unless separately proven persistent.
- Keep held-weapon drop and extra corpse-loot weapon roll separate.
- Attack speed remains safety-sensitive.
- For loot patch builders, scope edits to an exact named sub/object block; do not use ambiguous global first-match anchors.

## Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** confirmed NOT persistent.

## Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine as initially inserted: rejected after it removed corpse loot interaction.
2. POC-002B global first-match resource-anchor patching: rejected; item landed in `Resin_FT` instead of `Biter_CommonResources`.

## Unknowns / next investigations

1. Whether POC-002C delivers Shock T4 while preserving normal Biter looting.
2. Whether native Shock T4 damage/durability effects persist after save/reload and uninstall.
3. Exact persistent per-item field/mechanism suitable for Ascension stage L+0..L+5.
4. Best implementation for Legendary Core as a genuine item/action.
5. Global 30% rarity gacha across intended weapon sources without overfilling inventory.
6. Destructible props that genuinely own loot tables.
7. Manual Save Anywhere input hook + safe native save trigger path.

## next_safe_action

**Run POC-002C on the TEST SAVE.**

Required order:

1. Install POC-002C; it may safely replace the known POC-002B artifact directly.
2. Confirm ordinary Biter corpses still show the loot interaction.
3. Loot several ordinary Biters until Shock T4 appears.
4. Before installing Shock, record Camp Axe damage/durability and current Poison/Freeze state.
5. Install Shock T4 into the test Tip socket and record the changed stats.
6. Save, quit, reload with POC-002C still installed and re-check.
7. Only if reload is green, uninstall POC-002C and reload the same save.
8. Record separately whether Shock UI/socket, damage bonus, and durability bonus persist.

Do not proceed to full Ascension/Core/global gacha until this persistence result is known.