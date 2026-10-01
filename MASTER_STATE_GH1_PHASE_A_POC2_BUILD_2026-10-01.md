# THE BEAST PROJECT — GH1 PHASE A POC2 BUILD RECORD

Date: 2026-10-01
Status: TEST-PENDING
Depends on: `MASTER_STATE_GH1_PHASE_A_PARTIAL_LOCK_2026-10-01.md`

Artifact:
`GH1_FEATURE_A_POC2_DROP_SHAREABLE_GATE_READY.zip`

Artifact SHA256:
`3f0ef62e829f2ec35f6e8a713a6b73133bcc943d3fbb06886b265dc339c38175`

Purpose:
- preserve the runtime-proven universal dismantle behavior from POC1,
- test the next isolated Drop gate only.

POC2 changes:
- preserve/ensure `CanDrop(true)` on the player-facing melee/firearm/outfit target set,
- force/add `IsShareable(true)` on that same target set,
- also patch eligible player-facing dynamic weapon definition blocks,
- do not modify `DismantleResult` declarations.

Safety:
- POC1 must already be installed,
- installer validates current `data4.pak` against the exact POC1 hash stored in `_GH1_FEATURE_A_STATE.json`,
- exact POC1 `data4.pak` is backed up before POC2,
- whole-file and per-block guards abort if any `DismantleResult` declaration changes,
- POC2 uninstall restores exact POC1 data4,
- Sense core entries are verified in output,
- no data2/data3 modification.

Runtime status:
- Dismantle: GREEN from POC1 and must remain GREEN.
- Drop: TEST-PENDING under POC2.

Next runtime check:
- Drop melee,
- Drop firearm,
- Drop bow/crossbow,
- Drop outfit,
- smoke-test one weapon dismantle and one outfit dismantle for regression only.
