# POC-002 — Persistent per-item upgrade probe

## Goal

Test whether a native weapon-mod/crafting effect can alter one existing Legendary weapon per instance and whether the resulting damage/durability state survives save/reload and ultimately mod removal.

Target test item: the persistent Camp Axe produced by POC-001.

Test upgrade: `ShockMod_PowerAttack_FT_T4`, which is a native orange/T4 Tip mod and exposes native increased-damage and increased-durability crafting effects.

## POC-002 initial build — FAILED loot delivery

The initial test build retained the POC-001 Camp Axe test definition and added a custom loot subroutine for the Shock T4 mod. Runtime report: ordinary dead Biters lost the `F` loot interaction entirely. This delivery method is rejected.

Do not reuse the custom `POC002_AscensionTestMod` loot-subroutine approach on the Biter object without a separately validated reason.

## POC-002B — loot interaction restored, Shock not delivered

POC-002B restored vanilla Biter `LootAmount` and vanilla Biter outer loot-pool structure, removing the custom subroutine. The intent was to add Shock T4 to `Biter_CommonResources`.

Post-build audit after the user killed 100+ zombies without receiving Shock found a patch-builder bug: the injector used a global first-match `Craft_Resin` anchor and inserted the Shock item into `Resin_FT`, not `Biter_CommonResources`.

Therefore the absence of Shock drops in 002B is explained and is not evidence about loot weight semantics.

## POC-002C — current test build

POC-002C rebuilds the loot side from vanilla 1.71E files and performs a scoped block edit:

- keeps vanilla Biter `LootAmount` unchanged;
- keeps the vanilla Biter outer loot-pool structure unchanged;
- does not add a custom loot subroutine;
- injects `ShockMod_PowerAttack_FT_T4` only inside the existing `Biter_CommonResources` set;
- uses a very high internal item weight (`1000.0`) only to shorten the test;
- preserves the POC-002 inventory/inventory-gen changes needed for the Camp Axe socket/effect probe.

Local POC-002C `data2.pak` SHA-256:

`5eea00f64c213b469ce250e08a24285d92aa00f942c99fe2784df7e057bb18fb`

The binary artifact remains local-only and must not be committed.

## Required runtime order

1. Install POC-002C on the test save.
2. Confirm ordinary Biter corpses remain lootable.
3. Loot several ordinary Biters until Shock T4 appears.
4. Before installing Shock, record Camp Axe damage/durability and current Poison/Freeze mod state.
5. Install Shock T4 into the test Tip socket.
6. Record changed stats and Modify screen.
7. Trigger a normal save, quit, reload with POC-002C installed, and re-check.
8. Only after reload passes, uninstall POC-002C and reload the same save.
9. Record separately whether the Shock mod UI/socket, damage bonus, and durability bonus persist.

Do not interpret socket persistence as equivalent to stat/effect persistence; POC-001 already proved definition-added sockets can disappear after uninstall while persisted item stats remain.