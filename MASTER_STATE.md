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

**PHASE 1C — POC-001 native Legendary identity and partial persistence confirmed.**

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
- Global container/enemy color sets are direct gacha tuning points.
- `crafting_effects.scr` exposes native damage/durability/swing-speed effects potentially reusable for Ascension.

## POC-001 — Native Legendary Opportunity/Camp Axe

Documentation: `patches/poc/POC_001_NATIVE_LEGENDARY.md`.

Test artifact: local-only `data2.pak`.

SHA-256:
`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

POC behavior:

- Modifies `dlc_ft_WPN_1HS_AXE_03_opportunity_r1` into Orange/Legendary test generation.
- Uses `Slashing_1h_Affixes_Legendary_ft` + `Weapons_Random_Legendary_ft`.
- Temporarily exposes four crafting sockets while mod is installed.
- Makes `Enemy_Lottery_Weapons` deterministic to the test item and raises ordinary Biter test lottery weight.
- Does not implement global gacha/Core/Ascension.

### Runtime results — confirmed

**With POC installed:**

- Game boot/load: PASS.
- Biter loot produced the test axe, displayed as **Camp Axe — Legendary One-Handed Axe**.
- Orange/Legendary identity: PASS.
- Legendary-style affixes: PASS.
- Durability/repair values: observed **160/160** and **7/7**.
- Modify screen exposed **Tip, Shaft, Grip, Charm** sockets while the POC definition was present.
- Save -> quit -> reload with POC still installed: PASS; Legendary identity, affixes, damage, durability, repairs, and four-socket modify structure remained.

**After uninstalling POC and loading the same save:**

- Weapon still displays **Legendary One-Handed Axe**: PASS persistent.
- Damage still **131**: PASS persistent.
- Legendary affixes remained: PASS persistent.
- Durability still **160/160**: PASS persistent.
- Repairs still **7/7**: PASS persistent.
- Extra Tip/Shaft/Grip sockets disappeared; only vanilla **Charm Socket** remained.

### Persistence conclusion

POC-001 proves that rarity/Legendary identity, rolled affixes, damage value, durability, and repair count are persisted on the weapon/save strongly enough to survive mod removal. However, socket availability added only by weapon definition is recomputed from vanilla definition after uninstall and therefore is **not** persistent by this method.

This distinction is now frozen knowledge for future design: persistent progression must use per-item/saveable properties or native persisted effects; definition-only structural changes cannot be assumed permanent.

## Technical invariants

- Do not commit original PAKs, vanilla extracted archives, or save files.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists just because it survives a reload with the mod installed.
- Treat definition-only sockets/structure as runtime-dependent unless separately proven persistent.
- Keep held-weapon drop and extra corpse-loot weapon roll separate.
- Attack speed remains safety-sensitive.

## Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for the tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** confirmed NOT persistent.

## Unknowns / next investigations

1. Exact persistent per-item field/mechanism suitable for Ascension stage L+0..L+5.
2. Whether native modification/effect systems can persist Ascension damage/durability boosts after uninstall.
3. Best implementation for Legendary Core as a genuine item/action.
4. Global 30% rarity gacha across all intended weapon sources without overfilling inventory.
5. Destructible props that genuinely own loot tables.
6. Manual Save Anywhere input hook + safe native save trigger path.

## next_safe_action

Proceed to a focused **POC-002 for persistent per-item upgrade state**, before implementing the full global gacha system.

POC-002 should test the smallest native/persistent mechanism that can alter one existing Legendary weapon's damage and durability per instance and survive save/reload, then uninstall if technically possible. If that path is confirmed, use it as the foundation for Legendary Core + Ascension. Do not use definition-only extra sockets as Ascension state.