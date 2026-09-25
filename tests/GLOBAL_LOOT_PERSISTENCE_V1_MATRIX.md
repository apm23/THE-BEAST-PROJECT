# GLOBAL LOOT PERSISTENCE V1 — runtime matrix

Candidate data2:

`32c129265ef9f9e2eb889946f91cff7119316e110c34180bc0d4cbbe60a54b7b`

Baseline control:

SPECIAL45 `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Status before user runtime report: **UNTESTED**.

## Safety preflight

- game closed before install/swap;
- current save backed up;
- do not test on the only copy of a valuable save;
- no Alpha3/Alpha4 registry experiment;
- no item-definition deletion/reorder;
- no inventory/versioning edits;
- no CP1/MultiMod during the first persistence proof.

## Matrix

| Step | State | Expected |
|---|---|---|
| A1 | Start game with candidate installed | No DLC-disabled warning; candidate data2 hash remains exact |
| A2 | Load Save A | Corpse `F` works; SPECIAL45 custom loot is active for newly spawned infected |
| A3 | Change scene/level in Save A | Newly spawned infected still use custom loot |
| B1 | Exit game completely | No save mutation tool involved |
| B2 | Replace with previously vanilla Save B | No mod file changes |
| B3 | Start game and load Save B | Custom loot immediately active for newly spawned infected |
| C1 | Exit game completely | Candidate still installed |
| C2 | Create New Game | Custom loot active without editing the new save |
| D1 | Different save slot / NG+ if available | Custom loot active |

## Required observations per state

- `F` corpse prompt present;
- weapon rarity behavior visibly differs from vanilla in the expected SPECIAL45 direction;
- resource quantities behave according to SPECIAL45, not vanilla 1-3 behavior;
- newly spawned entities are used for the test;
- no inventory disappearance;
- attack remains functional;
- save/reload does not change the data2 hash.

## Interpretation

### PASS

If A/B/C all pass, mark:

`GLOBAL_ROOT_V1 = RUNTIME-PROVEN across saves`

Then the project may begin porting later loot features onto this architecture while SPECIAL45 remains the historical proven gameplay baseline until a merged candidate passes its own runtime matrix.

### FAIL only on old/persisted entities

If newly spawned entities use custom loot but old entities/containers do not, the likely problem is serialized/generated loot instances rather than loss of global definitions. Do not rewrite loot tables again; investigate generation timing / entity persistence.

### FAIL on newly spawned entities after save change

If newly spawned entities revert to vanilla after Save B/New Game while the candidate PAK hash remains exact, root binding alone is insufficient. Next step is a narrow read-only investigation for the engine's loot initialization/reload event before considering an on-load/on-spawn hook.

### Filesystem mismatch

If candidate PAK changes/disappears, that is an install/loader problem, not a save-loot-definition problem.
