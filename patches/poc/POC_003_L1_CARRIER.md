# POC-003 — Legendary -> L+1 persistent carrier probe

Status: **BUILT — awaiting in-game persistence validation**

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

A **newly generated** POC-003 Camp Axe must be used. Do not reuse the old POC-001/002 axe when deciding this result.

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

The supplied installer recognizes known older weapon POC hashes. If any unknown `data2.pak` exists, installation stops instead of overwriting it. This specifically protects parallel Manual Save Anywhere work or any unrelated mod/test package.

The uninstaller removes `data2.pak` only when its SHA-256 exactly matches POC-003.

## Required runtime order

Use a disposable/copied test save.

1. Make sure no Manual Save POC or unrelated package currently owns `ph_ft\source\data2.pak`.
2. Install POC-003 and confirm the installer reports the expected POC-003 hash.
3. Launch 1.71E and acquire a **new** Camp Axe from the controlled Biter path.
4. Confirm it is a genuine Orange/Legendary Camp Axe and that Shock is already installed.
5. Record, before doing anything else:
   - displayed damage;
   - durability/max durability;
   - repairs;
   - rarity and rolled affixes;
   - visible Shock state/effect.
6. Store/retrieve the weapon once if practical, then re-check stats.
7. Trigger a normal save, quit fully, restart with POC-003 still installed, and inspect the exact same weapon.
8. If the with-POC reload passes, save/quit again and run the POC-003 uninstaller.
9. Launch clean vanilla 1.71E and inspect the exact same weapon again.
10. Record whether Shock still exists/works and whether the **POC-specific damage/durability values** remain unchanged.

## Interpretation

### Strong pass

After POC removal, the same item retains:

- Legendary identity/affixes;
- installed Shock state;
- the exact POC-003 damage value;
- the exact POC-003 max durability value;
- normal inventory/equip/stash behavior.

Interpretation: strong evidence that a native installed-mod carrier can serialize non-vanilla Ascension parameters per item. This becomes the preferred foundation for real L+1 state before extending to L+2..L+5.

### Partial pass

Shock remains installed/functioning after POC removal, but damage and/or durability changes to the values implied by the vanilla Shock T4 definition.

Interpretation: the carrier identity persists, but its parameters are definition-resolved after load. Do **not** claim arbitrary persistent Ascension from this route. The next POC must find a different serialized per-item field/carrier strategy.

### Fail

The item corrupts, disappears, loses its installed-mod state, or causes save/inventory regressions.

Interpretation: stop and preserve POC-001/002 as the last frozen-green weapon state.

## Freeze rule

Do not advance to full Legendary Core, global Ascension, or L+2..L+5 from code inspection alone. POC-003 becomes green only after the complete:

`generate -> inspect -> save -> reload -> remove POC -> vanilla reload -> inspect`

protocol succeeds and the result is recorded in `MASTER_STATE.md`.
