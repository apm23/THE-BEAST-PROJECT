# POC-003 — Legendary -> L+1 persistent carrier probe

Status: **RUNTIME COMPLETE — custom stat signature did not survive uninstall**

Target: Dying Light: The Beast **1.71E**.

## Goal

Test the smallest remaining Ascension assumption without disturbing POC-001/002 frozen-green behavior:

> Can a native installed per-item weapon mod carry a deliberately non-vanilla L+1 stat signature into the save strongly enough that the signature survives after the POC definition patch is removed?

POC-002 already proved that the native installed mod/effect state itself can persist on one Legendary Camp Axe after the POC that exposed the socket is removed. POC-003 moves one step further: it tests whether **custom modifier parameters applied at installation/generation time** are serialized per item, or whether the game later resolves them again from the vanilla CraftPart definition.

This POC is a persistence probe only. It is **not** the final Legendary Core UI, final Ascension UX, or final L+1 balance.

## Test weapon and carrier

Weapon:

`dlc_ft_WPN_1HS_AXE_03_opportunity_r1`

Carrier:

`ShockMod_Random_FT_T4_TIP`

The Camp Axe uses the same controlled native-Legendary path proven by POC-001 and receives the carrier through the already-mapped native:

`StartupMod("ShockMod_Random_FT_T4_TIP")`

A **newly generated** POC-003 Camp Axe was used for the runtime result.

## Deliberate POC-003 signature

Vanilla Shock T4 uses the ordinary T4 crafting-effect parameters. For this test only, the exact Shock T4 CraftPart block is changed during generation to:

- `CraftingEffect_IncreasedDamageMul` level **8**;
- `CraftingEffect_IncreasedDurability` level **3** (`+18%` native durability effect);
- attack speed unchanged.

Level 8 damage is already defined by the vanilla 1.71E `crafting_effects.scr`; POC-003 does not invent a new engine effect.

The signature is intentionally different from vanilla so uninstall behavior is unambiguous. It must **not** be interpreted as the final L+1 tuning. The current project target envelope remains approximately **+12% damage / +15% durability**, with attack speed conservative.

## Patched paths

The local PAK contains exactly four paths:

- `scripts/inventory/inventory_gen.scr`
- `scripts/inventory/inventory.scr`
- `scripts/inventory/loot/lootsets_ft.loot`
- `scripts/inventory/loot/lootpools_ft.loot`

Changes are scoped to exact named blocks:

1. the Opportunity/Camp Axe r1 generated item;
2. the native `ShockMod_Random_FT_T4_TIP` CraftPart block;
3. `Enemy_Lottery_Weapons` for deterministic test identity;
4. only the ordinary `Biter` object's two pre-existing weapon-lottery calls, raised for short test acquisition.

The deterministic/boosted loot changes are test-only. Final gacha must restore the full weapon pool and frozen RNG targets.

## Builder

Project-authored builder:

`tools/build_poc003_l1_carrier.py`

The builder consumes the user's own extracted 1.71E baseline and does not redistribute vanilla source files.

Static build gates:

- exact-anchor edits only;
- source/patched brace counts must match;
- original UTF-8 BOM state preserved;
- original newline style preserved;
- PAK ZIP integrity check must pass;
- PAK member list must be exactly the four expected paths.

## Local-only artifact

`data2.pak` SHA-256:

`5608ecb1336ca84c80bc1472000ab9b50eb79a94a8a6a6c1b127f370cd31e17a`

User-test package SHA-256:

`a1eee27144a7ac612d0600bce57fa117d3ea8a915ca8ca258ae1615b13655a59`

The binary PAK/package remains local-only and is not committed to this public repository.

## Coexistence safety

POC-003 uses `ph_ft\source\data2.pak`, so it must **not** be active at the same time as another test that also owns that path.

The supplied installer recognizes known older weapon POC hashes. If any unknown `data2.pak` exists, installation stops instead of overwriting it. The uninstaller removes `data2.pak` only when its SHA-256 exactly matches POC-003.

## Runtime result

Detailed runtime record:

`tests/results/POC_003_RUNTIME_UNINSTALL_RESULT.md`

### Initial / with POC-003 active

The newly generated Legendary Camp Axe showed:

- damage **147**
- durability **160/188**
- repairs **7/7**
- affixes `+6% Damage (Infected)`, `+20% Damage (Accessories)`, `-7.5% Stamina Cost (Melee Weapons)`
- **Spark — Applies SHOCK on critical hits** visible

### Save -> quit -> reload with POC-003 still installed

**PASS.**

The exact same item remained at:

- damage **147**
- durability **160/188**
- repairs **7/7**
- same affixes
- Spark / SHOCK still visible

### POC-003 uninstall -> vanilla reload

The same saved item then showed:

- Legendary rarity preserved
- same listed affixes preserved
- damage **147 -> 142**
- max durability **188 -> 185** while current durability remained **160**
- repairs remained **7/7**
- POC-added Tip/Shaft/Grip UI disappeared; only vanilla Charm Socket remained
- Spark UI text disappeared with the definition-added socket exposure
- the Shock hardware/visual attachment still appeared attached in the supplied runtime screenshot
- post-uninstall SHOCK proc functionality was not directly combat-tested in this comparison

## Interpretation

### Strong pass — REJECTED

The exact POC-specific damage and max-durability values did **not** survive POC removal.

Therefore a native installed-mod identity plus temporary custom CraftPart parameters is **not** sufficient as an arbitrary persistent Ascension-stat carrier.

### Carrier persistence — PARTIAL EVIDENCE

The weapon itself remained valid, Legendary identity/affixes/repairs persisted, and the physical Shock attachment remained visible. This remains compatible with POC-002's conclusion that installed native mod state can serialize strongly.

However, the custom modifier magnitude is still definition-dependent rather than proven serialized per item. Post-uninstall SHOCK combat behavior remains unconfirmed for this exact POC-003 item.

## Frozen consequence

- POC-001 and POC-002 remain frozen green.
- POC-003 is **not green for arbitrary L+1 stat persistence**.
- Do not extend this parameter-override strategy to L+2..L+5.
- Do not claim the POC-003 custom L+1 values survive uninstall.
- The next Ascension POC must find a different serialized per-item field/state or another native carrier whose magnitude itself is stored on the item instance.
