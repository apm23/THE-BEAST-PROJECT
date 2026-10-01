# THE BEAST PROJECT — GH1 PHASE A FULL GREEN LOCK

Date: 2026-10-01
Status: RUNTIME PROVEN / GREEN
Scope: GH1 single-player expansion, Phase A only

## User runtime confirmation

The user explicitly confirmed, in sequence:

1. Universal dismantle works for **all tested weapons and outfits**.
2. POC1 Drop was not yet proven.
3. POC2 added the missing Drop/shareability gate while preserving dismantle behavior.
4. The user then explicitly reported: **"drop proven"**.

Therefore Phase A is now FULL GREEN.

## Locked proven behavior

- Player-facing weapons can be dismantled.
- Player-facing outfits/clothing can be dismantled.
- Player-facing weapons can be dropped.
- Player-facing outfits/clothing can be dropped.
- The Phase A implementation remains layered on the already-installed GH1 stack, preserving GH1 Sense/XRay and the rest of the current stack.

## Proven implementation lineage

### POC1 — Universal Drop + Dismantle foundation
Artifact:
`GH1_FEATURE_A_UNIVERSAL_DROP_DISMANTLE_POC1_READY.zip`

Artifact SHA256:
`a7ceb5b19282c03d4a6ccf86ae06e34e4d958fdc87c537d51676ed04bc9093f3`

Runtime result:
- weapon dismantle: GREEN
- outfit dismantle: GREEN
- drop: not yet GREEN at this stage

### POC2 — Drop/shareability gate
Artifact:
`GH1_FEATURE_A_POC2_DROP_SHAREABLE_GATE_READY.zip`

POC2 design:
- POC1 must already be installed,
- validates current data4 against the POC1 state file,
- keeps the POC1 dismantle routes unchanged,
- keeps/forces `CanDrop(true)`,
- adds/forces `IsShareable(true)` for the same player-facing weapon/outfit targets,
- backs up exact POC1 data4 and can restore it safely.

Runtime result:
- drop: GREEN / PROVEN by explicit user report.

## Phase A final status

**PHASE A = COMPLETE / RUNTIME GREEN.**

Do not reopen or redesign Phase A by default. Preserve its proven behavior in every later GH1 expansion build.

If later work changes inventory definitions, any file that contains Phase A targets must preserve:
- proven dismantle routing,
- `CanDrop(true)`,
- `IsShareable(true)` where required for the proven Drop behavior.

## Current development contract

Continue one feature at a time:
1. keep the current installed GH1 + Phase A GREEN state,
2. build Phase B as a separate reversible overlay,
3. runtime-test Phase B,
4. lock only after explicit user confirmation,
5. continue to Phase C/D/E,
6. no total compile until all requested functions are individually GREEN,
7. final compile happens during/after the planned fresh DLTB reinstall,
8. CO-OP work resumes only after the single-player consolidated build is stable.

## Next safe action

**Phase B: weapon acquisition -> corresponding native weapon blueprint.**

Start conservatively with native blueprint families that already exist in game data and use the game's own `LinkedItems("Craftplan_...")` mechanism. Preserve weapon identity and do not begin rarity/Legend scaling yet; that belongs to Phase C.
