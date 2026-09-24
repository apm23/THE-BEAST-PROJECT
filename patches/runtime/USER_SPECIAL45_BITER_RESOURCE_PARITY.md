# USER SPECIAL45 — Biter Resource Parity Candidate

Status: **CANDIDATE / NOT RUNTIME GREEN**

This profile is derived from the exact canonical **USER HIGH LOOT SPECIAL45** payload for Dying Light: The Beast 1.71E.

Canonical parent `data2` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

## Goal

Make the ordinary Biter crafting-resource drops such as Battery, Wiring, Oxidizer, Cleaning Supplies, etc. have the **same internal selection weight as Scrap**, while preserving the proven corpse routing.

This candidate intentionally does **not** alter `LootedObject("Biter")` topology or its outer route weights.

## Safe patch scope

Only this canonical SPECIAL45 file is changed:

`scripts/inventory/loot/lootsets_ft.loot`

Only these existing named sub-pools are replaced:

- `Biter_CommonResources`
- `Biter_Resources`

`scripts/inventory/loot/lootpools_ft.loot` remains byte-identical to canonical SPECIAL45 and is used only to verify the frozen Biter route.

The outer ordinary Biter routes remain frozen:

- normal: `Biter_CommonResources` weight `20.0`
- normal: `Biter_Resources` weight `10.0`
- PermaWorld: `Biter_CommonResources` weight `23.0`
- PermaWorld: `Biter_Resources` weight `11.0`

No corpse branch is added, deleted, reordered, or renamed.

## Resource parity rule

Both Biter resource sub-pools contain the same crafting-resource set below, and every listed crafting resource uses internal weight `5.0`.

| Resource | Quantity | Weight |
|---|---:|---:|
| `Craft_Scrap` | 40-55 | 5.0 |
| `Craft_Rags` | 33-50 | 5.0 |
| `Craft_Wiring` | 33-50 | 5.0 |
| `Craft_Container` | 33-50 | 5.0 |
| `Craft_Resin` | 33-50 | 5.0 |
| `Craft_Blades` | 33-50 | 5.0 |
| `Craft_Weights` | 33-50 | 5.0 |
| `Craft_Feathers` | 33-50 | 5.0 |
| `Craft_Leather` | 33-50 | 5.0 |
| `Craft_Battery` | 33-50 | 5.0 |
| `Craft_Cleaning_Supplies` | 33-50 | 5.0 |
| `Craft_Oxidizer` | 33-50 | 5.0 |
| `Craft_Alcohol` | 33-50 | 5.0 |
| `Craft_Fuel_Can_FT` | 33-50 | 5.0 |

This first candidate is deliberately restricted to resource types already present in the canonical SPECIAL45 Biter resource graph.

`Craft_Electrical_Parts`, `Craft_Pigments`, and `Craft_Firearm_Scrap_FT` are not added in this candidate because they were not part of the existing ordinary-Biter resource set.

Existing extras are preserved:

- `Cash_Cash` remains in `Biter_CommonResources`.
- `Plant_Poppy` and `Plant_Cordyceps` remain in `Biter_Resources` at weight `0.5`.

Because both Biter crafting-resource sub-pools contain the same crafting-resource set with the same internal weight, the listed crafting materials have equal relative selection chance to Scrap across the existing Biter resource routes.

## Builder

Run after the verified 1.71E local baseline has been extracted:

```powershell
python .\tools\build_user_special45_biter_resource_parity.py
```

Or:

`tools\BUILD_1.71E_USER_SPECIAL45_BITER_RESOURCE_PARITY.cmd`

Output:

`local_build/USER_SPECIAL45_BITER_RESOURCE_PARITY/data2_payload.pak`

The builder first reconstructs canonical SPECIAL45 and requires its exact parent hash before applying the candidate patch.

It also verifies the frozen `LootedObject("Biter")` route in untouched `lootpools_ft.loot` and fails if those routes no longer match the expected SPECIAL45 structure.

## Runtime gate before promotion

Do not mark this profile proven until all of these pass in NORMAL mode:

1. no `DLC ITEMS DISABLED`;
2. ordinary corpse `F` interaction still works;
3. ordinary Biters visibly yield the intended Battery/Wiring/Oxidizer/etc. resource mix;
4. quantities remain Scrap `40-55`, non-Scrap `33-50`;
5. save/reload is stable;
6. standard/special weapon loot behavior is unchanged;
7. `data3` recipe overrides still work.

After NORMAL passes, test `COOP_MULTIMOD` and confirm joining the vanilla sibling world still works.

Canonical SPECIAL45 remains the rollback/proven baseline until this candidate passes runtime testing.
