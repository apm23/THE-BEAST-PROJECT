# THE BEAST PROJECT — GH1 PHASE B RECOVERY + POC2

Date: 2026-10-01
Status: ACTIVE AUTHORITATIVE ADDENDUM

## 1. ROLLBACK RESULT

User explicitly confirmed that after uninstalling rejected Phase B POC1, the game returned to normal:
- player body/visual state normal again,
- weapon identities normal again,
- stash contents normal again,
- stacked/common-axe corruption gone,
- Phase A baseline restored.

Therefore the rollback path is runtime-confirmed.

## 2. PHASE A REMAINS GREEN

Do not regress or uninstall the current Phase A POC2 baseline while Phase B is under development.

Runtime-GREEN:
- universal player-facing weapon dismantle,
- universal player-facing outfit dismantle,
- universal player-facing weapon drop,
- universal player-facing outfit drop.

## 3. PHASE B POC1 IS REJECTED

Rejected approach:
- broad inventory-script reconstruction in data4,
- mass addition of `LinkedItems("Craftplan_...")` across many weapon definitions.

Observed failure symptoms:
- player body parts/visual state disappeared,
- weapons lost identities,
- many weapons collapsed into stacked common axes,
- stash weapons disappeared/collapsed.

This branch must not be retried.

## 4. NEW SAFE STRATEGY FOR PHASE B POC2

POC2 must NOT modify any weapon definition or inventory item definition.

Instead, prove the engine-native acquisition behavior using a weapon that ALREADY has a native blueprint link in vanilla/current game data.

Known native example:
`dlc_ft_wpn_15hs_volatile_r1`
contains:
`LinkedItems("Craftplan_dlc_ft_wpn_15hs_volatile_T1_Blueprint");`

Native blueprint chain exists for that family (T1/T2/T3) and is versioned by the game.

POC2 test method:
1. Leave all inventory definitions untouched.
2. Temporarily modify only the effective `scripts/inventory/loot/lootsets_ft.loot`.
3. Reuse the existing `Enemy_Lottery_Weapons` sub; do not create a new LootedObject or new topology branch.
4. Inject one already-native-linked weapon into that existing weapon set with dominant weight.
5. Raise only the existing Viral -> `Enemy_Lottery_Weapons` route weight so the test weapon is easy to obtain from a Viral corpse.
6. Preserve `LootedObject` count, existing topology, GH1 resource systems, Sense, Phase A gates, weapon definitions, stash/versioning, rarity/damage data.
7. After pickup, test whether the already-native `LinkedItems` route unlocks the blueprint and whether it persists after save/reload.

If native-linked pickup does NOT unlock the blueprint, stop treating `LinkedItems` as a proven pickup-unlock mechanism and research another native grant route.

If it DOES work, lock the acquisition mechanism before expanding coverage.

## 5. POC2 SAFETY RULES

- Exact Phase A POC2 state/hash gate before installation.
- No `inventory_gen.scr`, `inventory_ranged.scr`, weapon-definition, outfit-definition, versioning or stash modifications.
- Only one effective loot file may change: `scripts/inventory/loot/lootsets_ft.loot`.
- No new `LootedObject` blocks.
- No new loot sub/topology branch; reuse `Enemy_Lottery_Weapons`.
- Backup exact pre-test data4.
- Uninstall restores exact Phase A POC2 data4.
- Phase B remains TEST-PENDING until explicit user runtime confirmation.

## 6. NEXT SAFE ACTION

Build and runtime-test Phase B POC2 loot-only native-link probe.
