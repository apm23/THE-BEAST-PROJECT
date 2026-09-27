# MASTER_STATE — SURVIVOR SENSE / ESP CONTINUATION — 2026-09-27

## Authority / how to use this file

This file is the **latest continuation override for the Survivor Sense / ESP work** in `apm23/THE-BEAST-PROJECT` on branch `remake-proven45`.

Read the repository `MASTER_STATE.md` first for the broader THE BEAST PROJECT gameplay/loot/CO-OP history, then read this file completely before continuing Survivor Sense / ESP work.

This file intentionally records the full runtime-research state from the long 2026-09-27 chat so a fresh chat must **not restart old experiments**.

### Continuity keyword

`BEAST-SENSE-ESP-V38R1`

Interpret that exact keyword as:

> Continue THE BEAST PROJECT Survivor Sense / custom ESP investigation from the 2026-09-27 V38.1 state. Preserve all proven runtime chains and failed-hypothesis history below. Do not restart V24-V36 branch guessing. Treat custom external ESP as the current primary direction. Inspect actual GitHub HEAD and both master-state files before taking action.

Short alias accepted by the user for this sub-project:

`SENSE38`

If a fresh chat receives either `BEAST-SENSE-ESP-V38R1` or `SENSE38`, it should immediately reconstruct this state and continue from `next_safe_action` below instead of asking the user to repeat project history.

---

# User goal / acceptance criteria

Primary gameplay goal:

- Dying Light: The Beast current runtime build used in this investigation is approximately **1.71PE**; older project baseline material was 1.71E.
- User wants **all living infected visible through walls**, including ordinary Biters that built-in Survivor Sense sometimes omits.
- Viral and all specials must be included.
- Indoor / outdoor / near / far / sleeping / resting / dormant infected should be included.
- Hostile humans are required; friendly humans are optional.
- Target effective range roughly **200 m**.
- Target visible duration roughly **20 s** if built into Survivor Sense; for a custom ESP, persistent while enabled is acceptable unless user says otherwise.
- Dead AI is not required.
- Final desired visual is wall-through visibility comparable to ESP/X-ray; exact native Survivor Sense implementation is no longer mandatory.
- After Sense/ESP is solved, user wants to revisit bullet wall penetration / wallhack bullets. **Do not work on bullets until ESP/Sense is solved.**

User context / workflow constraint:

- User wants to finish quickly because sibling is waiting to play co-op.
- User is tired of repeated blind A/B branch tests and long scanners.
- Prefer direct, narrow, verified collectors and finished ZIP artifacts.
- Do not repeatedly ask permission when next action is obvious.
- Keep instructions short and practical.

---

# Hard runtime safety rules for this sub-project

1. Do not touch save/versioning/stash/DLC-sensitive gameplay files for Sense/ESP research.
2. Runtime probes should be read-only whenever possible.
3. Any temporary code-memory patch must:
   - exact-byte verify before write;
   - patch the smallest possible bytes;
   - auto-restore;
   - restore in `finally` / failure path;
   - never alter save/PAK state.
4. No more broad whole-private-heap PowerShell scans. They were slow and unreliable.
5. Prefer direct known pointer chains and narrow native-code context extraction.
6. Do not revive already disproven V24-V36 hypotheses unless new evidence specifically contradicts the failure.
7. Built-in Survivor Sense is no longer the primary architecture. Custom ESP is now preferred.
8. Never claim a runtime route GREEN until the user actually reports visible success.

---

# Golden gameplay context that must remain separate

The broader gameplay/loot baseline remains in main `MASTER_STATE.md`.

Important related known-safe state from this chat:

- Golden V2 inventory / loot / Exotic / Night Sovereign / stack 99999 / slots lineage is historically proven.
- Golden V3 flashlight + silent firearm lineage is historically proven.
- Historical V3 local artifact: `DLTB_G1_GOLDEN_V3_FLASHLIGHT_SILENT_FIREARM.zip`.
- Historical frozen V2 DATA2 SHA-256: `eaad5c091fe83648047e00039e1378b976438aa867ec3856bcd6aee10fa77258`.
- Historical DATA3 SHA-256: `89ce4faf81c6e47295efd5f8e3bd2e461902a130900f28ef8f05d225faa71931`.
- Total-backup tool historically used: `DLTB_TOTAL_GOLDEN_SNAPSHOT_TOOL_V2_FIXED.zip`.

These gameplay packages are **not** the subject of the current ESP work. Do not mutate them merely to debug Sense.

---

# Survivor Sense observations before runtime probing

Observed runtime problem:

- Survivor Sense can X-ray some ordinary Biters but omit other visually identical ordinary Biters standing near them.
- Near/far does not explain the omission.
- Some ordinary Biters visible through walls and some not, even in the same scene.
- Dead Volatile could appear in X-ray during one test, showing dead-state filtering and Biter omission are separate questions.

Nexus Survivor Sense mod reference used during investigation:

- root `survivor_sense.scr` approach was tested.
- settings included concepts like `IncludeNotSpawnedAIs=true` and `SkipDeadAIs=false`.
- root-path testing did not solve the ordinary-Biter omission.

Static-game-source finding:

Base Biter metadata includes:

- `m_PerceptionProfile = biter_dlc_ft`
- `m_ConflictSide = zombie`
- `m_ModulesPreset = modules_biter_anger`
- `m_MainBehaviorTree = BITER_BT`
- `m_AnimationPreset = biter_tactical@ai_animation_presets.scr`
- `m_PerceptionPreset = infected`
- `m_InitBehaviorTree = biter_init_tree_base`

Relevant static source also showed `biter_tactical` animation preset uses the Biter graph and Human binding namespace.

Key conclusion:

**The missing ordinary Biter is not absent because it lacks the expected base Biter static preset.** Runtime state/filtering is involved.

---

# Direct runtime pointer chain — PROVEN / KEEP

The most reliable direct runtime chain recovered in this investigation:

```text
gamedll_ph_x64_rwdi.dll base = module
manager = *(module + 0x3ACB4F0)
LevelDI-like = *(manager + 0x138)
SenseState = LevelDI-like + 0x2518   // EMBEDDED, not a pointer
A = *(LevelDI-like + 0x15B0)
B = *(A + 0x2468)
```

This chain repeatedly resolved in milliseconds and is substantially more reliable than private-heap scanning.

Important correction from V25.3 -> V25.4:

- `LevelDI + 0x2518` is an **embedded SenseState object**.
- Do **not** dereference it as a pointer.

Example historical live values from one run:

- LevelDI-like vtable/live mapping was observed around `gamedll RVA 0x2AAD058`.
- embedded Sense XYZ sample approximately `(0.07, 6.88, -0.39)`.

These example addresses are ASLR/session-specific except the module-relative/static RVAs explicitly noted.

---

# Survivor Sense source container — PROVEN existence

Earlier direct source-list chain used:

```text
A = *(LevelDI + 0x15B0)
B = *(A + 0x2468)
source container around B + 0xA10
```

This returned roughly 36-39 source records in typical tests.

Important semantic discovery:

- The entries returned by the source container are **source records/wrappers**, not direct HumanAI actor pointers.
- Source-record addresses frequently ended in `...070`.
- Native strings inside these records exposed AI animation/preset identity.

Example strings found directly in source records:

- `biter_tactical@ai_animation_presets.scr`
- Viral animation preset strings
- Spitter / Goon and other infected-related strings

Critical conclusion:

**Ordinary Biters that fail X-ray are already present in the direct Survivor Sense source container.**

Therefore the problem occurs **after source construction** — in later filtering/state/visualization/rendering — not because the Biter is absent from the source list.

---

# V24 / V24.1 — model proxy attempts — FAILED

Goal:

- Attempted to alter model/proxy identity so an ordinary Biter would be treated like a known X-ray-visible special infected.

Result:

- Ordinary Biter did not physically change into Volatile.
- `m_AIModelName` / HumanAI model proxy route was not the runtime visual identity path controlling the observed Biter.

Status:

**Rejected. Do not restart this route.**

---

# V25 lineage — direct chain and wrapper discovery

## V25

- Tried nearest-actor resolution by distance using private heap scan.
- Too broad/slow and owner resolution failed.

## V25.1

- Tried direct vtables.
- Owner resolution still failed.

## V25.2

- Direct pointer chain improved.
- Initial compile warning-as-error from unused `managerBase` fixed.
- Then failed due overly strict LevelDI vtable check.

## V25.3

- Removed strict vtable validation.
- Failed because SenseState was incorrectly treated as a pointer.

## V25.4 — IMPORTANT SUCCESS

- Corrected SenseState to embedded `LevelDI + 0x2518`.
- Direct chain READY in roughly 3 ms.
- Source-list direct chain worked.
- Confirmed source entries are not direct HumanAI pointers.

## V25.5

- Wrapper resolver searched ~2 levels.
- Resolved `0/N` source records to HumanAI actor pointers.

## V25.6

- Tried `sourceEntry - 0x70` because records ended in `...070`.
- Still `0` HumanAI.

## V25.7

- Local 0x4000 slab resolver found exact `HumanAI`-related vtable and appeared to produce a distance.
- Later analysis proved this was a false actor-base interpretation.
- It matched a secondary HumanAI-related subobject near `sourceEntry + 0x80` and then read unrelated data as actor world position.

Status:

**Distance/nearest-target route is abandoned.**

---

# Known vtable RVAs from native inspection

Historical exact module-relative vtable RVAs observed:

- Skinned visualizer VT: `gamedll + 0x290F550`
- Morphed visualizer VT: `gamedll + 0x290F580`
- HumanAI-related VT: `gamedll + 0x29633A0`

Important correction:

The HumanAI-related VT found at source-record `+0x80` was a **secondary subobject**, not proof that the source-record base itself was the actor.

Do not use it as a world-position base without new proof.

---

# V26 / V26.1 — active visualizer pool hypothesis — FAILED

## V26

Goal:

- Correlate Sense source record to currently active X-ray visualizer pool.

Problem:

- Active Skinned pool resolver returned zero despite visible X-ray targets in game.

## V26.1

- Searched candidate pools around SenseState `+0x80 .. +0x180` using exact Skinned/Morphed vtables.
- Result: `poolCandidates=0`, `actorUnion=0`.

Conclusion:

- The visualizer pool location/layout assumption was wrong.
- Source-record parsing remained useful.

Status:

**Do not revive the same pool offsets.**

---

# Kill-event targeting — major methodological improvement

User suggested using intentional kills instead of unreliable distance matching.

This was adopted and worked much better.

Rationale:

- User can choose a visible target manually.
- Tool watches which source record disappears from Sense container after the kill.
- The removed source record becomes a reliable event anchor for the killed target.

This avoids nearest-actor ambiguity.

---

# V27 — Kill Pair Tracer

Artifact:

`DLTB_SENSE_V27_KILL_PAIR_TRACER.zip`

User result:

`DLTB_SENSE_V27_KILL_PAIR_RESULT_20260927_085315.zip`

Important result:

- Kill #1 non-Xray source entry: `0xCB502C7C070`
- Kill #2 Xray source entry: `0xCB502A34070`
- Both had native name `biter_tactical@ai_animation_presets.scr`
- Both reported `RemovedFromSource=True`
- Sense source count dropped by one after each kill.

Conclusion:

**Source-record removal is a valid death-event anchor.**

Weakness:

- Stage timing/arming was awkward, motivating V28 manual/event-driven staging.

---

# V28 — Quad Kill Correlator — IMPORTANT DATASET

Artifact:

`DLTB_SENSE_V28_QUAD_KILL_CORRELATOR.zip`

SHA-256:

`0366445262069d4e79973ce0952775f0b62c1a2f3d4da0845b8e351953d2cd17`

User result:

`DLTB_SENSE_V28_QUAD_KILL_RESULT_20260927_090258.zip`

Design:

- Four manually armed stages; no countdown.
- `NON_XRAY_1`
- `NON_XRAY_2`
- `XRAY_1`
- `XRAY_2`
- Each stage waited indefinitely for one relevant source-record removal.
- Captured 0x1000 source record, pointer graph, module pointers/RVAs, strings, byte/qword discriminator tables.

Captured identities:

```text
NON_XRAY_1 = 0xCB502C7C070 | biter_tactical@ai_animation_presets.scr
NON_XRAY_2 = 0xCB5036C0070 | viral_dlc_ft@ai_animation_presets.scr
XRAY_1     = 0xCB502820070 | biter_tactical@ai_animation_presets.scr
XRAY_2     = 0xCB502C7C070 | biter_tactical@ai_animation_presets.scr
```

Important limitation:

- `NON_XRAY_2` was a **Viral**, not a Biter.
- Therefore the nominal 2-vs-2 class comparison was imperfect.

Extremely important same-slot observation:

- `NON_XRAY_1` and `XRAY_2` reused the exact same source-record address `0xCB502C7C070` at different times.
- This allowed comparing **the same source-record slot/state** when non-Xray vs Xray.

Perfect byte discriminator found by the original class table:

- `+0x830`: non-Xray `1`, Xray `0`.

Same-address cluster details:

NON_XRAY_1:

```text
+0x828 bytes: 0a31000102010101
+0x830 bytes: 0101000000000000
```

XRAY_2:

```text
+0x828 bytes: 0a31000002000000
+0x830 bytes: 0001000000000000
```

Changing bytes in the six-byte logical cluster beginning at `+0x82B`:

- `+0x82B`: 1 -> 0
- `+0x82C`: stays 2
- `+0x82D`: 1 -> 0
- `+0x82E`: 1 -> 0
- `+0x82F`: 1 -> 0
- `+0x830`: 1 -> 0

`+0x831` stays `1` and is not part of the changing set.

Full same-slot byte-diff regions observed across the 0x1000 capture included:

- `0x1A4-0x1A7`
- `0x1A9-0x1AB`
- `0x21D-0x21F`
- `0x224-0x227`
- `0x229-0x22B`
- `0x5BC-0x5BE`
- `0x6C8-0x6CB`
- `0x70D-0x70F`
- `0x714-0x715`
- `0x719-0x71B`
- `0x73C`
- `0x740-0x743`
- `0x748-0x74B`
- `0x82B`
- `0x82D-0x830`
- `0xF68`
- `0xFA8-0xFAA`
- `0xFB4-0xFB8`
- `0xFBC-0xFBE`
- `0xFF0-0xFF3`

Interpretation:

- The cluster is a strong **state marker/correlation**.
- Causality was not yet established.

---

# V29 — +0x830 single-flag causal test — FAILED

Artifact:

`DLTB_SENSE_V29_BITER_FLAG830_TEST.zip`

SHA-256:

`00f3e493e3eb515ed4ac27eb91618bb36e6583518b1cbf70d319ce704cc637cb`

Method:

- Select Biter source record by native preset string.
- If `+0x830 == 1`, temporarily force to `0` for ~15 s.
- Auto-restore.

User runtime result:

**No visual change.**

Conclusion:

`+0x830` alone is **not a sufficient causal X-ray gate**.

---

# V30 — Biter flag-cluster causal test — FAILED

Artifact:

`DLTB_SENSE_V30_BITER_FLAG_CLUSTER_TEST.zip`

SHA-256:

`c91b33099b0b5258b49b18e8ee4c600464c43f811342579fdf3d9cec28e34fce`

Method:

Match exact non-Xray signature:

```text
[+0x82B .. +0x830] = [1,2,1,1,1,1]
```

Force changing bytes to Xray-correlated zeros:

- `+0x82B = 0`
- `+0x82D = 0`
- `+0x82E = 0`
- `+0x82F = 0`
- `+0x830 = 0`

Leave `+0x82C = 2` unchanged.

User runtime result:

**No visual change.**

Conclusion:

The V28 cluster is a **marker/consequence or non-sufficient state**, not the direct controlling gate.

Status:

**Do not continue blind source-record flag patching.**

---

# Synsteric cheat table evidence — major clue, but old build

User uploaded:

`Synsteric's DLTB Cheat Table 1.1.5 451 1.1.5 2026-06-14T13-25Z EKkvjkRHj.zip`

Important entry found in the table:

`Force X-Ray`

Old script structure:

```asm
aobscanmodule(ForceXray,gamedll_ph_x64_rwdi.dll,
0F 84 ?? ?? ?? ?? 49 8B 0F C6 44 24)

ForceXray:
db 0F 80
```

Old recorded injection location:

`gamedll_ph_x64_rwdi.dll + CE0099`

Semantics:

- Old script changed a long conditional jump from `0F 84` (`JE/JZ`) to `0F 80` (`JO`) while retaining the rel32 target.
- This strongly suggests an old native decision branch controlled X-ray eligibility.

Cheat Engine UI observation:

- `Force X-Ray` was under a DEV/testing tree, around `[DEV] Testing -> maybe later idk -> Force X-Ray`.
- User could not activate/click it on current build.
- Expected explanation: old AOB no longer matches current build and/or script is obsolete for current executable.

The old exact AOB was searched in current DLL and was not found.

---

# V31 — native outer-gate hypothesis — FAILED

A current function around `gamedll + 0xAC630B` appeared superficially similar to the old Force X-Ray pattern.

Observed code shape included:

```asm
cmp byte ptr [rcx+1A52],0
je  ...
xor r9d,r9d
mov byte ptr [rsp+20],2
mov r8b,1
mov rdx,rsi
call ...
```

V31A:

- patched only final candidate branch around `AC630B`.

V31B:

- patched three `[rcx+1A52]` gates around `AC61DD`, `AC62CB`, `AC630B`.

User runtime result:

**A and B both no change.**

Conclusion:

Those outer gates are not the missing-Biter X-ray controller.

---

# V32 — inner visual state-machine hypothesis — FAILED

Tracing the V31 call path reached helper around:

`gamedll + 0xB9BF50`

Interesting code appeared to select/update states near `0x100 / 0x101 / 0x102`, with guards around `B9C00D` / `B9C011` and virtual calls around `[rbx+F8]` / `[rbx+100]`.

V32A:

- bypassed an inner visual update guard.

V32B:

- forced presumed `mode == 2` path plus update.

User runtime result:

**Both no change.**

Conclusion:

This state machine is not sufficient to control the missing ordinary-Biter X-ray behavior.

Status:

Do not continue patching nearby branches based only on apparent visual-state semantics.

---

# V33 — broad Force-Xray signature locator

Artifact:

`DLTB_SENSE_V33_CURRENT_FORCE_XRAY_LOCATOR_FIXED.zip`

Purpose:

- Scan current `gamedll_ph_x64_rwdi.dll` on disk.
- Search exact old wildcard and generalized nearby structural patterns.

Initial V33 build had a PowerShell parser bug:

```text
Sort-Object Score -Descending, Offset
```

Fixed build used proper multi-property Sort-Object syntax.

User result:

`DLTB_SENSE_V33_FORCE_XRAY_LOCATOR_RESULT_20260927_095235.zip`

Conclusion:

- No exact old wildcard.
- Broad structural candidates were too noisy / false-positive prone.

---

# V34 — exact structural locator

Artifact:

`DLTB_SENSE_V34_EXACT_STRUCTURAL_FORCE_XRAY_LOCATOR.zip`

User result:

`DLTB_SENSE_V34_STRUCTURAL_RESULT_20260927_141216.zip`

Search shape tightened to old adjacent instruction structure:

```text
Jcc
immediately followed by REX.W MOV r64,[r/m64]
immediately followed by C6 44 24 disp8 imm8
```

Also searched short-Jcc variants and MOV+stack-write pairs.

V34 produced roughly **120 structural candidates**.

Conclusion:

Structural similarity alone is still insufficient; many unrelated functions compile to the same local shape.

---

# V35 — V34 candidate #5 test — FAILED

Candidate #5 looked semantically closer to old table because it contained:

```asm
0F 85 ...
49 8B 02
C6 44 24 60 01
```

V35 correctly converted V34 raw file offset -> PE RVA -> live VA before patching.

Patch mirrored old table strategy:

- `0F 85` -> `0F 80`
- preserve branch displacement
- 18 s auto-restore

User runtime result:

**No change.**

Candidate #5 rejected.

---

# V36 — V34 candidates #1 and #3 — FAILED

Re-ranked candidates by semantic similarity:

Candidate #1:

```asm
0F 84 A0 00 00 00
48 8B 0E
C6 44 24 40 0E
```

Candidate #3:

```asm
0F 84 00 01 00 00
48 8B 08
C6 44 24 4C 00
```

Both matched old branch type `JE (0F84)` and performed real memory dereference into RCX before stack-byte write.

V36A tested candidate #1.

V36B tested candidate #3.

Both changed `0F84 -> 0F80`, preserved rel32, exact-byte verified, auto-restored.

User runtime result:

**Both failed / no visible change.**

Final conclusion from V31-V36:

**Stop code-shape lookalike patching.**

The old Force X-Ray clue remains useful historically, but current equivalent cannot be found reliably by local byte-shape similarity alone.

---

# Architecture pivot — custom ESP instead of built-in Survivor Sense

After V24-V36 failures, user delegated direction and asked for a practical solution quickly.

Decision:

**Primary path is now a custom ESP independent of Survivor Sense.**

Target architecture:

```text
live AI enumeration
    -> stable AI identity/type
    -> world XYZ
    -> camera/view-projection
    -> world-to-screen
    -> transparent overlay / through-wall marker
```

Advantages:

- bypasses built-in Survivor Sense filtering entirely;
- can include every Biter regardless of native X-ray eligibility;
- can include hostile humans;
- can use custom range and colors;
- no need to mutate game AI state to force native X-ray.

Desired final implementation should preferably be external/read-only if practical.

---

# V37 — AI Hook Context Collector — IMPORTANT NATIVE CONTEXT

Artifact:

`DLTB_ESP_V37_AI_HOOK_CONTEXT_COLLECTOR.zip`

User result:

`DLTB_ESP_V37_AI_HOOK_CONTEXT_RESULT_20260927_152020.zip`

V37 searched current DLL for old cheat-table AI-related native hooks, including concepts corresponding to:

- Change AI Scale
- Freeze/Kill Nearby AIs
- Set AI Position Fix
- Spawn AI
- Survivor Sense entry

Important interpretation from V37 native context:

A nearby-AI function contains a container-like structure around offsets near:

```text
+0x8D8
+0x8DF
+0x8E0
```

Native code also accesses an element-related value around `entry + 0x10` and a transform-related global/table.

Initial hypothesis from V37:

```text
[B + 0x8D8]  -> tagged AI-related container/array pointer
[B + 0x8DF] / [B + 0x8E0] -> count-ish metadata
entry + 0x10 -> transform handle/index-ish field
```

This hypothesis motivated V38.

Important caution after V38/V38.1:

**Do not call `[B+0x8D8]` a proven flat qword AI pointer array.**

The container is definitely interesting and live, but its exact element layout remains unresolved.

---

# V38 — Active AI Transform Probe — PARTIAL / COUNT ASSUMPTION WRONG

Artifact:

`DLTB_ESP_V38_ACTIVE_AI_TRANSFORM_PROBE.zip`

User result:

`DLTB_ESP_V38_ACTIVE_AI_TRANSFORM_RESULT_20260927_153716.zip`

Runtime values from that session:

```text
AIArrayTagged = 0x10102BF2D753650
masked pointer = 0x2BF2D753650
CountByte     = 0x01
Count32       = 1043466322   // clearly not a sane AI count
```

V38 bug:

- Script interpreted `CountByte=1` as encoded `count = byte - 1` and therefore selected `0` entries.
- Nearby 32-bit value was obviously garbage as a count.

Conclusion:

- tagged pointer at `B+0x8D8` is real/interesting;
- **count encoding assumption copied from older Sense source-list logic was wrong for this container.**

V38.1 was built to scan slots directly without relying on count.

---

# V38.1 — Active AI Array Recovery — LATEST USER RESULT

Artifact:

`DLTB_ESP_V38_1_ACTIVE_AI_ARRAY_RECOVERY.zip`

User result:

`DLTB_ESP_V38_1_ACTIVE_AI_ARRAY_RESULT_20260927_155116.zip`

Exact runtime metadata from result:

```text
module  = 0x7FFC5FC30000
manager = 0x2BA814B1020
LevelDI = 0x2C0D06B7C80
A       = 0x2BAED0FDDC0
B       = 0x2BF2D752D70
AIArrayTagged = 0x10102BF2D753650
AIArray       = 0x2BF2D753650
TagUpper16    = 0x101
RecoveredEntries = 20
```

V38.1 also dumped `B+0x880 .. +0x97F`.

Critical post-result analysis:

The direct qword-slot scan **did not recover 20 clean AI actor pointers**.

Examples from snapshot:

- one plausible live source-record-like pointer: `0xCB50209C070`
- one plausible object with string `_Crawler` and `l_Resting`
- several module/static pointers such as `0x7FFC625297E8`
- obvious non-pointer/small encoded values such as:
  - `0x400000004`
  - `0x646BE`
  - `0x5071B`
  - `0x312D3900`
  - `0x300000003`
  - `0x100000001`
  - `0x3E00000017`
  - `0x10000000017`
  - `0x2000000000`
  - `0x302F343C`
  - `0x40800000`

One entry `0xCB50209C070` had a vtable-like first qword and data patterns similar to the already-known source-record family.

Another entry `0x2BF01D49390` exposed readable strings including `_Crawler` and `l_Resting`.

Interpretation:

**V38.1 proves the tagged object/container is not a simple contiguous `AIEntry*[]` of qwords.**

The scan was reading mixed container metadata/inline values/subobjects because the element stride/layout was wrong.

Therefore:

- `RecoveredEntries=20` must **NOT** be interpreted as 20 AI actors.
- Do not build overlay from those qword slots yet.
- Do not assume `entry+0x10` transform handle for the qword-scanned values.

This is the latest state at chat rollover.

---

# What V38.1 DOES prove

1. The direct root chain `module -> manager -> LevelDI -> A -> B` still resolves correctly in the current session.
2. `B+0x8D8` contains a stable tagged pointer-like value with upper tag `0x101` and masked address `0x2BF2D753650` in the captured session.
3. The pointed structure is readable and contains mixed live/native data relevant to nearby-AI processing.
4. The element/container representation is **not a flat qword pointer vector**.
5. V37 native disassembly context must be used to recover the exact stride / tag decode / element access semantics instead of guessing from memory layout.

---

# Current strongest evidence about target identity

Across the whole investigation:

- Non-Xray Biter and Xray Biter can share exact native animation preset string `biter_tactical@ai_animation_presets.scr`.
- The same source-record slot address was observed at different times in both non-Xray and Xray states.
- Source-state byte cluster correlates with Xray state but forcing it did not produce Xray.
- Therefore the distinction is runtime state / downstream filter / renderer behavior, not a simple static Biter-vs-special identity flag.
- This supports the custom-ESP pivot: enumerate living AI directly instead of trying to reproduce native filter logic.

---

# Rejected / do-not-repeat list

Do NOT restart these without genuinely new evidence:

- V24 model proxy / `m_AIModelName` visual identity path.
- V25 private-heap nearest actor scan.
- V25.7 sourceEntry+0x80 secondary HumanAI subobject as actor world-position base.
- V26/V26.1 guessed visualizer pools near SenseState offsets.
- V29 single `+0x830` patch.
- V30 `+0x82B..+0x830` cluster patch.
- V31 `[rcx+1A52]` outer-gate patching.
- V32 presumed inner visual state-machine patching.
- V33 broad structural signature scoring as a patch-selection method.
- V35 candidate #5.
- V36 candidates #1/#3.
- treating V38/V38.1 `B+0x8D8` target as a flat `AIEntry*[]`.

---

# Tooling / scripting lessons from this chat

PowerShell pitfalls to preserve:

- Never use helper function name `H`; it aliases `Get-History`.
- Use a distinct helper such as `Get-TBPHash` when needed.
- Never repurpose automatic `$matches`.
- Empty `byte[]` behavior can collapse to `$null`; handle zero-length arrays explicitly.
- Multi-property `Sort-Object` syntax must use property expressions; the V33 parser failure came from `Sort-Object Score -Descending, Offset`.

Runtime tool UX preferences:

- CMD launcher beside PowerShell/C# source.
- clear active/restored/fail-safe messages.
- short runtime windows for patches.
- auto-generated result ZIP.
- avoid requiring user to manually edit offsets.
- collectors should be quick and ideally read-only.

---

# Artifacts / result names from this Sense/ESP session

Keep these names for historical correlation even if local files are not committed:

- `DLTB_SENSE_V27_KILL_PAIR_TRACER.zip`
- `DLTB_SENSE_V27_KILL_PAIR_RESULT_20260927_085315.zip`
- `DLTB_SENSE_V28_QUAD_KILL_CORRELATOR.zip`
- `DLTB_SENSE_V28_QUAD_KILL_RESULT_20260927_090258.zip`
- `DLTB_SENSE_V29_BITER_FLAG830_TEST.zip`
- `DLTB_SENSE_V30_BITER_FLAG_CLUSTER_TEST.zip`
- `DLTB_SENSE_V31_NATIVE_FORCE_XRAY_BRANCH.zip`
- `DLTB_SENSE_V32_INNER_VISUAL_STATE_MACHINE.zip`
- `DLTB_SENSE_V33_CURRENT_FORCE_XRAY_LOCATOR_FIXED.zip`
- `DLTB_SENSE_V33_FORCE_XRAY_LOCATOR_RESULT_20260927_095235.zip`
- `DLTB_SENSE_V34_EXACT_STRUCTURAL_FORCE_XRAY_LOCATOR.zip`
- `DLTB_SENSE_V34_STRUCTURAL_RESULT_20260927_141216.zip`
- `DLTB_SENSE_V35_FORCE_XRAY_CAND5_TEST.zip`
- `DLTB_SENSE_V36_FORCE_XRAY_CAND1_CAND3_TEST.zip`
- `DLTB_ESP_V37_AI_HOOK_CONTEXT_COLLECTOR.zip`
- `DLTB_ESP_V37_AI_HOOK_CONTEXT_RESULT_20260927_152020.zip`
- `DLTB_ESP_V38_ACTIVE_AI_TRANSFORM_PROBE.zip`
- `DLTB_ESP_V38_ACTIVE_AI_TRANSFORM_RESULT_20260927_153716.zip`
- `DLTB_ESP_V38_1_ACTIVE_AI_ARRAY_RECOVERY.zip`
- `DLTB_ESP_V38_1_ACTIVE_AI_ARRAY_RESULT_20260927_155116.zip`

Known hashes explicitly captured in chat:

```text
V28 ZIP SHA256 = 0366445262069d4e79973ce0952775f0b62c1a2f3d4da0845b8e351953d2cd17
V29 ZIP SHA256 = 00f3e493e3eb515ed4ac27eb91618bb36e6583518b1cbf70d319ce704cc637cb
V30 ZIP SHA256 = c91b33099b0b5258b49b18e8ee4c600464c43f811342579fdf3d9cec28e34fce
V31 ZIP SHA256 = 443bb2fe39d5eb6606f8b03dcc53436849fdec1199c2891273fa0adc17281663
V32 ZIP SHA256 = ae952a9e6678aa4a47be809651d144ee495cbe629331a13fc3294944d2cd6193
V33 FIXED ZIP SHA256 = 3d53ea4d6283b8e605cd263f74c767fead0abce87c11413cfca6f5042402a4ba
V34 ZIP SHA256 = 3abd82ea31aae85f13f86a5faf2b3b238fc719d578f1ff4e3ce02fb27011cdfa
V35 ZIP SHA256 = c72a482f966e756d427a5ebcddd25643b10594126b92e5d817368d39509aa967
V36 ZIP SHA256 = 2b5ab4a21d401944cd5db72cb07e7a56c1a0d60e5108d4b158d320eabe0f00b1
V37 ZIP SHA256 = 8a9060f92a3d5879636cb1eb77115d66db4dfe3b01ba437c6c64e354774d07bc
V38 ZIP SHA256 = 25e1509311e04a233c8427b2fe9087ca7d02e584a35ff96e660a951ec7a4d1e8
V38.1 ZIP SHA256 = 70ff8e9d1e46b19fa4e42ee1597749ac0e9c9ee74ddd4835ef39be16ddcd3db7
```

---

# next_safe_action — CURRENT / AUTHORITATIVE

Do **not** create V38.2 by merely changing a guessed count or scanning more qwords.

Next action must use the **actual V37 native function semantics** to decode the container at/around `B+0x8D8`.

Recommended exact sequence:

1. Re-open / disassemble the V37 `FreezeAndKillNearbyAIs` context around every instruction that accesses `+0x8D8`, `+0x8DF`, `+0x8E0`.
2. Determine:
   - whether `+0x8D8` stores a tagged pointer, inline small-vector, pointer+count encoding, or another custom container;
   - exact element stride;
   - exact tag mask / tag semantics;
   - exact loop termination/count decode;
   - where the native code converts an element into an AI actor / transform handle.
3. Build a **read-only V39 decoder probe** that implements those exact native semantics.
4. V39 should dump, for each decoded element:
   - raw element bytes;
   - decoded actor/object pointer;
   - vtable RVA if module-backed;
   - relevant identity strings;
   - the exact transform/position field used by the game;
   - two or three snapshots for motion correlation.
5. Require a clean set of multiple infected entries before proceeding.
6. Only after AI enumeration is proven, resolve world XYZ.
7. Then identify camera/view-projection matrix and implement world-to-screen.
8. Then build external transparent ESP overlay.
9. Only after ESP works should hostile-human filtering / coloring / 200 m limit be refined.
10. Only after ESP is solved should bullet wall penetration work resume.

Preferred future overlay behavior:

- ordinary infected marker through wall;
- specials distinct if desired;
- hostile humans included;
- dead actors ignored by default;
- 200 m maximum range;
- stable frame-rate impact;
- read-only process access if possible.

---

# Fresh-chat startup checklist

When a new chat starts with `BEAST-SENSE-ESP-V38R1` or `SENSE38`:

1. Inspect actual GitHub branch `remake-proven45` HEAD.
2. Read `MASTER_STATE.md` completely.
3. Read `MASTER_STATE_SENSE_ESP_2026-09-27.md` completely.
4. Treat this file as the newest authority for Survivor Sense / ESP work.
5. Do not ask the user to restate V24-V38 history.
6. Do not restart built-in X-ray branch guessing.
7. Confirm that the latest known user result is V38.1.
8. Remember V38.1's `RecoveredEntries=20` are mixed container values, **not 20 proven AI actor pointers**.
9. Continue by decoding the native nearby-AI container semantics from V37 context.
10. Keep the user-facing workflow direct and compact; sibling is waiting for co-op play.

---

# Current status in one sentence

**Built-in Survivor Sense forcing is abandoned after V24-V36 failures; custom ESP is now primary, direct root chain is proven, `B+0x8D8` is a live tagged nearby-AI-related container, V38.1 disproved the flat-qword-array assumption, and the next step is native-semantic container decoding from V37 followed by world XYZ and overlay.**
