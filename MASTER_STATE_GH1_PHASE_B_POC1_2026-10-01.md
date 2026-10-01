# THE BEAST PROJECT — GH1 PHASE B POC1

Date: 2026-10-01
Status: TEST-PENDING
Depends on: `MASTER_STATE_GH1_PHASE_A_GREEN_2026-10-01.md`

## Proven prerequisite

Phase A is FULL GREEN by explicit runtime confirmation:
- weapon dismantle: proven,
- outfit dismantle: proven,
- weapon drop: proven,
- outfit drop: proven.

Do not uninstall or redesign Phase A while Phase B is being tested.

## Phase B target

Long-term goal:
**obtaining a weapon should also provide/unlock its corresponding weapon blueprint.**

This POC only proves the native acquisition/link route first. It does not yet create a blueprint for every weapon family.

## Native evidence used

Game data already contains player weapons with:
`LinkedItems("Craftplan_..._T1_Blueprint")`

Native weapon craftplans use:
- `CraftplanType("Weapon")`,
- `ScaleWithPlayerRank(...)`,
- `ItemLevel(...)`,
- `NextLevelBlueprintName(...)`.

Therefore POC1 uses the game's existing weapon/blueprint link architecture rather than a save hack or temporary custom carrier.

## POC1 implementation

Artifact:
`GH1_PHASE_B_POC1_NATIVE_BLUEPRINT_LINK_READY.zip`

Artifact SHA256:
`fb3d7e12959b9dffdc64d5a250547335f38e5369a5f27a512dee6be8238b4c10`

Runtime builder behavior:
1. Requires the current Phase A POC2 state file.
2. Verifies current `data4.pak` equals the exact Phase A POC2 installed hash saved in state.
3. Scans effective inventory scripts across active `dataN.pak` precedence.
4. Finds native blueprint definitions with `CraftplanType("Weapon")` and names matching `Craftplan_<family>_T<n>_Blueprint`.
5. For each family, chooses the lowest native blueprint tier available (normally T1).
6. Finds exact matching player-facing melee/firearm weapon variants where the weapon family is the weapon id with trailing `_r<number>` removed.
7. If the weapon block has no existing `LinkedItems(...)`, appends `LinkedItems("<lowest native blueprint>")`.
8. If a different `LinkedItems(...)` already exists (for example ammo), the weapon is skipped and reported instead of guessing multi-link syntax.
9. Guards Phase A invariants: dismantle route, `CanDrop`, and `IsShareable` must remain unchanged.
10. Preserves the current data4 payload, including Sense/XRay and Phase A, then overlays only changed inventory scripts.
11. Does not modify data2/data3.
12. Creates `Documents\GH1_PHASE_B_POC1_MATCHES.txt` listing patched weapon -> blueprint pairs and skipped existing-link cases.
13. Uninstall restores the exact Phase A GREEN data4 only if the current Phase B hash still matches; otherwise STOP SAFE.

## Runtime test required

Choose a weapon listed in `GH1_PHASE_B_POC1_MATCHES.txt` whose blueprint is not already owned.

Test:
1. obtain/pick up the listed weapon,
2. verify the corresponding native blueprint appears/unlocks,
3. save/reload,
4. verify the blueprint remains available.

Do not mark this POC GREEN until the user explicitly confirms both acquisition and persistence.

## Next step if GREEN

Lock the native `LinkedItems` acquisition route, then expand Phase B coverage to weapon families that currently lack an exact native matching blueprint and handle existing `LinkedItems` conflicts in a separately tested pass.
