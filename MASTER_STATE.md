# MASTER_STATE

## Authority

This file plus the actual GitHub HEAD are the source of truth for project continuation. Reconcile both before making changes. Do not reconstruct state from chat memory when repository state disagrees.

## Current baseline

- Game: **Dying Light: The Beast**
- Target build observed in-game: **VER. 1.71E**
- Installation state at baseline: **fresh install, no mods installed**
- Clean test save captured: `save_ft_0.sav`
- Clean test save SHA-256: `82af1723995ab086853934f67551b7ac61e2f7587191a4952d6e04c3e15ee4d5`
- Save file itself must remain local/private and must not be committed.
- Clean archive map observed `data0.pak,data1.pak`.
- Targeted 1.71E extraction completed locally: **58 requested files, 0 missing**.

## Current phase

**PHASE 1B — POC-001 built; awaiting in-game native-Legendary validation**

A test-only `data2.pak` has been built. Global gacha, Legendary Core, and Ascension are **not implemented yet**.

## Frozen project goals

1. Universal native Legendary eligibility for weapons even when vanilla caps them at Rare/Epic.
2. Global per-weapon rarity gacha, target initial Legendary roll ~30% when a weapon instance is generated.
3. Slightly increased weapon availability from common infected, humans, searchable/destructible loot sources that actually own loot definitions.
4. Human held-weapon drop participates in the same rarity roll; the actual weapon being carried may become Legendary.
5. Legendary rarity should be a real item state/quality, not merely cosmetic text/color.
6. Legendary Core item/progression mechanic.
7. Rare/Epic + Core -> native Legendary when technically possible.
8. Legendary + Core -> per-item Legendary Ascension progression L+1 through L+5.
9. Ascension emphasizes damage and durability; secondary stats increase more conservatively; attack-speed changes must stay animation/hit-registration safe.
10. Progression should be per weapon instance, not a global buff for every weapon of the same definition.
11. Persistence is a hard requirement to investigate and test: obtained Legendary/Ascension state should survive mod removal wherever the engine/save format permits.
12. Keep RNG/farming; do not force every drop to Legendary.

## Initial balance targets

- Legendary chance per generated weapon: **30%** initial target.
- Common Biter weapon availability target: approximately **20–25%**, subject to actual loot semantics and inventory pressure.
- Human held-weapon drop: **preserve vanilla 1.0 where confirmed**; do not reduce to the earlier conceptual 60–75% target.
- Extra human corpse-weapon lottery: tune separately from held-weapon drop.
- Legendary Core target chances:
  - common infected: 8–10%
  - Viral/human: ~10%
  - special infected: 12–15%
  - ordinary containers: 8–10%
  - good/locked chest: 12–15%
  - boss/Chimera: 20–30%
- Core costs:
  - Rare/Epic -> Legendary: 1
  - Legendary -> L+1: 1
  - L+1 -> L+2: 2
  - L+2 -> L+3: 3
  - L+3 -> L+4: 5
  - L+4 -> L+5: 8

## Confirmed 1.71E mapping

See `docs/BASELINE_1.71E_MAPPING.md` for detail.

### Native rarity identity

- Blue = Rare.
- Violet = Epic.
- Orange = Legendary.
- Platinum and Exotic exist above Orange.
- Named loot objects confirm the mapping: Rare uses Blue-only, Epic uses Violet-only, Legendary uses Orange-only.

### Weapon architecture

Confirmed relevant files:

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

Generated weapon rank instances contain stable `UID`, rank/tier fields, damage-tier linkage, and explicit forced/random affix-group names.

Native Legendary generated weapons use Legendary-specific affix groups such as class-specific `*_Affixes_Legendary_ft` plus `Weapons_Random_Legendary_ft`.

Lower-rarity generated weapons can hardcode Rare affix groups. Therefore Universal Legendary must not be implemented as a cosmetic recolor only.

### Human held weapons

Standard inspected human weapon-set presets use `OverrideWeaponDropDurabilityParams()` with `LootChance(1.0)` for the held weapon. The mod should preserve this where present and apply gacha/native-rarity handling to the dropped held weapon itself.

### Corpse/loot paths

- `Biter` and `Viral` corpse pools are resource-heavy and already contain a separate extremely small Orange-only `Enemy_Lottery_Weapons` path (vanilla weight `0.05`).
- Several standard human corpse pools contain a separate Orange-only `Enemy_Lottery_Weapons` path at even smaller weight (`0.002`), independent of held-weapon drop.
- `ColorSet_DLC_FT_Generic_Container`, `ColorSet_DLC_FT_DH_Container`, `ColorSet_DLC_FT_Enemy_Base`, `ColorSet_DLC_FT_Enemy_Advanced`, and related sets are direct global-gacha tuning points.

### Upgrade/Ascension

`weaponenhancmentcosts.scr` exposes costs per rarity/type but not the complete stat-growth or persistence model. `crafting_effects.scr` exposes native damage/durability/swing-speed effects that may be reusable for Ascension. Per-item persistent Ascension encoding is still unresolved.

## POC-001 — Native Legendary Opportunity Axe

Documentation: `patches/poc/POC_001_NATIVE_LEGENDARY.md`.

Built test artifact: `data2.pak` (kept out of the public repo).

SHA-256:

`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

POC behavior:

- modifies only `dlc_ft_WPN_1HS_AXE_03_opportunity_r1` into an Orange/Legendary test instance;
- uses `Slashing_1h_Affixes_Legendary_ft` and `Weapons_Random_Legendary_ft`;
- gives four crafting slots and T3 Slash dismantle result;
- temporarily makes `Enemy_Lottery_Weapons` deterministic to that test item;
- raises only ordinary Biter weapon-lottery weight from `0.05` to `15.0` in its two existing branches to make testing practical;
- does not yet alter global rarity/color sets, humans, Virals, containers, Core, or Ascension.

Static checks before packaging:

- PAK ZIP integrity passed;
- brace counts match vanilla for all three modified files;
- original CRLF line endings preserved;
- no UTF-8 BOM introduced.

## Technical invariants

- Do not commit original `data*.pak`, extracted vanilla archives, save files, or other copyrighted game dumps.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never claim persistence until uninstall/reload testing proves it.
- Never fake Universal Legendary by only recoloring/relabeling lower rarity.
- Do not globally overwrite all copies of a weapon when a per-instance upgrade path is technically available.
- Treat attack speed separately from damage/handling because excessive animation speed may break hit behavior.
- Keep human held-weapon drop and extra corpse-loot weapon rolls as separate tunable systems.

## Confirmed artifacts

- Repository: `apm23/THE-BEAST-PROJECT`.
- `README.md` defines baseline and authority order.
- `PROJECT_CONTRACT.md` freezes non-negotiable behavior and continuation protocol.
- `FEATURE_SPEC.md` records the agreed feature set and initial tuning envelope.
- `TEST_MATRIX.md` defines proof-of-concept, statistical, integrity, and uninstall/persistence tests.
- `config/balance.json` contains project-authored initial probabilities, Core costs, and Ascension targets.
- `tools/validate.py` statically validates probability/config bounds.
- `.github/workflows/validate.yml` is present for GitHub Actions validation.
- `tools/collect_baseline.ps1` can locally enumerate relevant paths from `data*.pak` without committing game archives.
- `.gitignore` blocks PAKs, saves, extracted baselines, and local baseline output.
- `docs/BASELINE_1.71E_MAPPING.md` records confirmed clean-baseline semantics without redistributing vanilla files.
- `patches/poc/POC_001_NATIVE_LEGENDARY.md` records POC-001 behavior and test plan.

## Unknowns to resolve

1. Whether the existing lower-rarity FT item can behave as a true Orange/Legendary instance with the mapped item-level overrides at runtime.
2. Whether rarity/affixes/crafting-slot state persist on the item after save/reload and after POC removal, or are recomputed from vanilla definitions.
3. Exact per-item save fields available for Ascension level.
4. Whether Legendary Core is best as a genuinely new inventory item or a safe reuse/extension of an existing item/action category.
5. Which destructible props actually own loot tables versus visual-only destruction.
6. Whether any upstream AI rule reduces the confirmed `LootChance(1.0)` held-weapon setting in practical gameplay.

## Failed hypotheses

None yet.

## Frozen-green systems

None yet. A system becomes frozen-green only after validator + in-game tests pass and evidence is recorded.

## next_safe_action

**Run POC-001 in-game on the TEST SAVE.**

Required order:

1. Install the exact POC-001 `data2.pak` identified by the SHA-256 above.
2. Confirm the game boots and the test save loads.
3. Kill/loot ordinary Biters until `Opportunity Axe` drops.
4. Record whether it is Orange/Legendary and whether Legendary affixes / four crafting slots are actually present.
5. Save, quit, reload with POC installed and re-check the same item.
6. If steps 1–5 are green, back up that modified test save and perform the controlled uninstall persistence test.
7. Record the exact persistence result before changing any global gacha/drop system.

Do **not** proceed to global 30% Legendary gacha, Core, or Ascension until POC-001 runtime identity and persistence behavior are known.
