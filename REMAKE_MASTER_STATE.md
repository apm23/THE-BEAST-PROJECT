# REMAKE MASTER STATE — PROVEN45 / 1.71PE

This file is the authority for branch `remake-proven45`. It overrides older Legendary Core / Ascension / A3 inventory text in the historical `MASTER_STATE.md` for this branch only.

## Current target

- Game runtime: **DLTB 1.71PE**.
- Current phase: **single-player core first**.
- Sense: **DEFERRED**.
- One-sided CO-OP: **DEFERRED**.
- Runtime status of the new 1.71PE package: **CANDIDATE_NOT_RUNTIME_GREEN** until local in-game hard gates pass.

## Immutable foundation

Global loot must be rebuilt from canonical **USER HIGH LOOT SPECIAL45**, never from Global Loot Root V1.

Canonical SPECIAL45 data2 SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

The current builder reconstructs this foundation first and rejects the build if the canonical hash drifts.

## Active feature contract

1. Preserve SPECIAL45 loot behavior and corpse topology.
2. Native weapon rarity path through **Exotic**.
3. Human enemies use project corpse/search loot like the zombie corpse system; do not add a held-weapon-drop feature.
4. Special infected retain controlled high-tier / Exotic opportunity.
5. Night Sovereign powerful outfit using the proven six native Vanguard carriers.
6. Inventory targets: Equipment `34`, Consumable `34`, Weapon `68`, Ammo `42`.
7. Material/consumable/throwable stack target: `99,999`.
8. Preserve dismantle support and proven drop/share definition normalization.
9. Preserve save/reload/scene behavior and corpse `F` / attack / ordinary controls.
10. Legendary Core and Legendary Ascension are **CANCELLED** for this remake.

## Recovered proven lineage

- stack 99,999 parent: `77e7ff5630167af4f733bda7e754ab0eb8f90c0491e75403caaeb64077a44155`
- Weapon68: `8b1587ce0741295e98598a2ea6e22fe67102a6b34644cacd14f7558ea09dde18`
- G1 weapon-access preflight: `6ee08e9d867a9a72b1968b557256747ac701c511f7580b0605f4cd3906e2b5c5`
- Night Sovereign G1: `047a44416f7ab8a1bb736cf2aac374a0cb36b96a0ff775ed05ff8ad2e73e4521`

Historical runtime proof retained from these lineages includes weapon drop+dismantle and Night Sovereign render/stat behavior. This does **not** by itself prove the transplanted 1.71PE build.

## Active build path

One command:

`tools\RUN_REMAKE_SINGLEPLAYER_CORE.cmd`

Flow:

1. extract current 1.71PE target files from the user's owned install;
2. compare against captured 1.71E contract;
3. require SPECIAL45 core byte compatibility, otherwise stop with a generated port plan;
4. rebuild canonical SPECIAL45 exactly;
5. context-transplant recovered G1 weapon/Exotic/Night Sovereign changes;
6. apply only narrow inventory/stack overrides to `player_variables.scr` and InventoryUpgrade_1/2 neutralization in `common_skills.xml`;
7. verify LootedObject name/order topology remains identical;
8. write candidate PAK + manifest;
9. package fail-safe install/status/rollback launchers;
10. package the runtime test recorder / promotion gate.

Active builder:

`tools/build_remake_proven45_recovered_candidate.py`

Recovered compact specs:

`patches/runtime/REMAKE_PROVEN45_G1_LEGACY/`

## Hard safety rules

- Never delete/reorder/rename live item definitions to chase compatibility.
- Never revive CP1 Alpha4.
- Never perform aggressive LootedObject structural rewrites.
- Never use Global Loot Root V1 as this remake's loot foundation.
- Do not patch `scripts/inventory/versioning/` or `stash_dlc.scr` in this phase.
- In `player_variables.scr`, only the committed inventory/stack allowlist may change.
- In `common_skills.xml`, only InventoryUpgrade_1 and InventoryUpgrade_2 slot/stack increments may be neutralized.
- Sense parameters must remain untouched while Sense is deferred.
- If a recovered context is ambiguous or absent on 1.71PE, stop instead of guessing.

## Runtime hard gates

Authority: `config/remake_singleplayer_test_matrix.json`.

Immediate hard failures include broken corpse `F`, broken attack/controls, save corruption/reload failure, DLC regression, or loot reverting after scene/save transition.

Runtime result recorder / promotion authority:

`tools/runtime_test_gate.py`

Convenience launcher:

`tools\RUNTIME_TEST_GATE.cmd`

The candidate package also includes `4_TEST_GATE.cmd` plus `runtime_test_gate.py` and `TEST_MATRIX.json`.

Promotion rule is strict:

- every T01–T15 must be recorded as `PASS`;
- zero hard-fail events may exist;
- only then may `promote` set `runtime_status` to `RUNTIME_GREEN`.

A FAIL or hard-fail leaves the package `CANDIDATE_NOT_RUNTIME_GREEN`. The gate does not auto-forgive or infer a pass.

## Next safe action

On the Windows machine containing the current 1.71PE installation, run:

`tools\RUN_REMAKE_SINGLEPLAYER_CORE.cmd`

If it produces `local_build\DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip`, install using the package's `1_INSTALL_CANDIDATE.cmd`, then execute T01–T15 and record each result with `4_TEST_GATE.cmd`.

Do not mark the remake runtime-green until `4_TEST_GATE.cmd promote` succeeds after all T01–T15 pass.
