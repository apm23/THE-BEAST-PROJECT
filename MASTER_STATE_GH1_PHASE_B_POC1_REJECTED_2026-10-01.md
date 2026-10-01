# THE BEAST PROJECT — GH1 PHASE B POC1 REJECTED

Date: 2026-10-01
Status: RUNTIME-FAIL / HARD REJECT / DO NOT REUSE

## Context

Baseline before this test was GH1 with Phase A POC2 installed and runtime-proven:
- universal weapon dismantle GREEN,
- universal outfit dismantle GREEN,
- universal weapon drop GREEN,
- universal outfit drop GREEN.

Phase B POC1 attempted to extend weapon acquisition with native-looking `LinkedItems("Craftplan_..._T1_Blueprint")` relationships by rebuilding effective inventory scripts into the active data4 overlay.

Artifact:
`GH1_PHASE_B_POC1_NATIVE_BLUEPRINT_LINK_READY.zip`

## Runtime result — HARD FAIL

User explicitly reported after installing Phase B POC1:
- all weapons became abnormal,
- parts of the player body disappeared,
- weapons disappeared,
- inventory weapon entries collapsed/appeared as many stacked common axes,
- weapons in stash disappeared.

Therefore Phase B POC1 is NOT PROVEN and must never be merged into GH1.

## Immediate recovery rule

Use the POC1 uninstaller to restore the exact Phase A POC2 data4 backup:
`2_UNINSTALL_PHASE_B_POC1.cmd`

Do NOT uninstall Phase A POC2 first.
Do NOT continue playing, dismantling, dropping, moving stash items, or testing Phase B while the broken Phase B data4 is active.

The Phase B uninstaller was designed to validate the current Phase B data4 hash before restoring the exact pre-Phase-B Phase A data4 backup.

If the uninstaller refuses because of a hash/state mismatch, do not overwrite files manually until the state file and backup path are inspected.

## Interpretation

The visible symptoms indicate that the Phase B approach affected inventory-definition resolution globally, not merely blueprint unlock behavior. The exact root cause is not yet proven and must not be guessed into master state.

Potential investigation dimensions for a later controlled redesign include:
- precedence/redefinition behavior when broad effective inventory scripts are copied into data4,
- whether copying whole inventory files changes item/UID resolution order,
- whether `LinkedItems` is safe only in original/native item definitions and unsafe in broad redefinition overlays,
- whether blueprint unlock requires a narrower reward/docket/collectable path rather than mass item-definition overrides.

These are hypotheses only, not established causes.

## Locked decision

REJECT:
- mass rebuild/override of broad weapon inventory definition files in data4 for universal blueprint linking,
- reusing Phase B POC1 as a base for later tests.

KEEP:
- Phase A POC2 as the last runtime-GREEN baseline.

NEXT SAFE ACTION after recovery is confirmed:
- verify inventory, stash, player body, weapon identities, Sense, Drop, and Dismantle returned to normal;
- only then design a much narrower Phase B experiment using one controlled native weapon/blueprint pair or a reward/unlock route without wholesale inventory redefinition.
