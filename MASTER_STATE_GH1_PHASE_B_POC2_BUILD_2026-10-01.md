# THE BEAST PROJECT — GH1 PHASE B POC2 BUILD RECORD

Date: 2026-10-01
Status: TEST-PENDING

Artifact:
`GH1_PHASE_B_POC2_LOOT_ONLY_NATIVE_LINK_READY.zip`

SHA256:
`1680f8e35fc36f4754d3d2c00015057b3fa14e349c056e09c74de975003b9a1d`

## Purpose

Safely test whether the engine-native `LinkedItems("Craftplan_..._T1_Blueprint")` behavior actually grants/unlocks a weapon blueprint when an already-native-linked weapon is acquired.

## Safety architecture

- requires exact current Phase A POC2 state/hash;
- rejected Phase B POC1 must already be uninstalled;
- does NOT modify `inventory_gen.scr`, `inventory_ranged.scr`, weapon definitions, outfit definitions, stash or versioning;
- discovers native-linked player weapons dynamically from current effective inventory scripts;
- user chooses one native-linked weapon/blueprint candidate at install time;
- modifies only the effective `scripts/inventory/loot/lootsets_ft.loot`;
- reuses existing `Enemy_Lottery_Weapons` sub;
- does not create new `LootedObject`, new sub, or new `use Enemy_Lottery_Weapons` branch;
- injects/boosts the chosen already-native-linked weapon inside the existing weapon lottery set;
- temporarily boosts the existing Viral -> `Enemy_Lottery_Weapons` route for deterministic testing;
- preserves all other current data4/Phase A/Sense content;
- backs up exact Phase A data4 and restores it on uninstall when hash safety passes.

## Static validation

- Python compile: PASS
- synthetic loot patch: PASS
- synthetic topology guard (`LootedObject` count, `sub` count, existing `use` count unchanged): PASS

## Runtime proof required

User must report:
- weapon/stash/player visuals remain normal,
- chosen test weapon drops from Viral,
- expected native blueprint unlocks on acquisition,
- blueprint persists after save/reload.

Do not mark Phase B mechanism GREEN until explicit runtime confirmation.
