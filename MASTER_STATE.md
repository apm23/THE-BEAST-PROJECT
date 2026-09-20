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

**PHASE 1 — clean vanilla mapping confirmed; controlled native-Legendary POC next**

No gameplay patch has been shipped yet.

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

## Unknowns to resolve

1. Whether a newly added mod-defined item with stable custom item name/UID persists safely in the save after the PAK is removed.
2. Whether the engine permits a lower-rarity FT weapon family to be cloned into a native Orange variant cleanly without additional hidden registration beyond the mapped inventory/versioning mechanisms.
3. Exact per-item save fields available for Ascension level.
4. Whether Legendary Core is best as a genuinely new inventory item or a safe reuse/extension of an existing item/action category.
5. Which destructible props actually own loot tables versus visual-only destruction.
6. Whether any upstream AI rule reduces the confirmed `LootChance(1.0)` held-weapon setting in practical gameplay.

## Failed hypotheses

None yet. Do not mark recolor-only as failed until tested; current mapping merely shows it would not satisfy the project’s native-affix requirement.

## Frozen-green systems

None yet. A system becomes frozen-green only after validator + in-game tests pass and evidence is recorded.

## next_safe_action

**Build the smallest controlled native-Legendary POC.**

Use one known lower-rarity FT melee family (initial candidate: `WPN_1HS_axe_03_opportunity`) and create one true Orange/Legendary test instance that preserves the same visual/weapon identity but uses:

- `Color_Orange`;
- class-appropriate `*_Affixes_Legendary_ft`;
- `Weapons_Random_Legendary_ft`;
- stable unique item name/UID;
- a deterministic or near-deterministic test loot route isolated from global balance.

Do not yet change global gacha/drop balance. First prove native Legendary identity, pickup/drop/stash/save/reload behavior, then perform the copied-save uninstall persistence test. Only after that proof is green should the generator/global loot work begin.
