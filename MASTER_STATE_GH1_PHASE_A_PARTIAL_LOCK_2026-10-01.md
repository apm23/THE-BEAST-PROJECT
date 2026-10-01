# THE BEAST PROJECT — GH1 PHASE A PARTIAL RUNTIME LOCK

Date: 2026-10-01
Status: AUTHORITATIVE RUNTIME RESULT ADDENDUM
Parent state: `MASTER_STATE_GH1_EXPANSION_2026-10-01.md`

## USER RUNTIME RESULT

Phase A POC1 artifact:
`GH1_FEATURE_A_UNIVERSAL_DROP_DISMANTLE_POC1_READY.zip`

POC1 artifact SHA256:
`a7ceb5b19282c03d4a6ccf86ae06e34e4d958fdc87c537d51676ed04bc9093f3`

User explicitly reported the following runtime result:

- **Dismantle — all tested weapons: PROVEN / GREEN.**
- **Dismantle — all tested outfits/clothing: PROVEN / GREEN.**
- **Drop — NOT WORKING / NOT PROVEN.**

This is a partial lock only. Do not mark all of Phase A complete yet.

## LOCKED FEATURE

The universal player-facing dismantle route introduced by Phase A POC1 is now treated as runtime-proven and must be preserved unchanged in later Phase A iterations.

Proven architecture to preserve:
- existing native `DismantleResult` system,
- existing native Slash / Blunt / Firearm / Ranged dismantle route families,
- conservative outfit fallback via native `Dismantle_T1_Blunt`,
- no structural `LootedObject` topology rewrite.

Any later Drop experiment must not remove, rewrite, or regress the working dismantle behavior.

## DROP STATUS / NEXT CONTROLLED HYPOTHESIS

POC1 set player-facing target items to `CanDrop(true)`, but runtime Drop still did not work.

Native game-data comparison shows droppable/shareable inventory examples commonly pair:
- `CanDrop(true)`
- `IsShareable(true)`

and locked examples can pair:
- `CanDrop(false)`
- `IsShareable(false)`

Therefore the next isolated Phase A test is to preserve every proven POC1 dismantle edit and change only the additional Drop/share gate by forcing `IsShareable(true)` on the same player-facing melee/firearm/outfit targets while retaining `CanDrop(true)`.

Do not alter `CanThrow`, loot frequency, item stats, armor stats, Sense, flashlight, firearm sound, save/versioning, inventory capacity, or blueprint progression during this test.

## NEXT SAFE ACTION

Build and runtime-test **Phase A POC2 — DROP SHAREABLE GATE**.

If POC2 Drop works:
- mark Drop GREEN,
- mark Phase A fully GREEN,
- lock exact POC2 build/hash,
- then begin Phase B.

If POC2 Drop still fails:
- keep dismantle GREEN,
- revert/replace only the Drop experiment,
- inspect the next native Drop/UI/world-spawn gate without touching the proven dismantle route.
