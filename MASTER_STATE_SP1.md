# MASTER_STATE_SP1

## Authority / relationship to `MASTER_STATE.md`

This file is the authoritative continuation checkpoint for the **DLTB Custom ESP / Sense reverse-engineering sub-project** as of 2026-09-28.

It supplements the existing root `MASTER_STATE.md` without replacing the older gameplay / G1.1 / CP1 history. For the ESP/Sense branch, this file is newer and wins where it conflicts with older notes.

## Continuation code

`SP1`

Interpret `SP1` as:

- resume the paused **DLTB Custom ESP / Sense** project from this exact checkpoint;
- do not ask the user to re-explain the history;
- inspect current GitHub HEAD and read both `MASTER_STATE.md` and `MASTER_STATE_SP1.md` before acting;
- preserve proven hooks/offsets and failed hypotheses below;
- continue from the latest safe action, not from earlier native-Sense or RAM-wide-camera experiments.

---

# User constraints / workflow contract

- User wants direct execution and short test steps.
- Avoid repeated clarification/permission loops.
- Avoid requiring DLTB relog/restart unless the game has actually crashed or a restart is technically unavoidable.
- Cheat Engine revisions should disable/restore cleanly where possible.
- The project moved to a **MASTER CT + hot-reload Lua patch** model specifically to avoid repeated inline re-hook/relog cycles.
- Patch file path used by MASTER:
  `C:\Users\USER\Documents\DLTB_ESP\BEAST_CUSTOM_ESP_MASTER_PATCH.lua`
- F2 hot-reloads the patch.
- Future patches should be delivered already named exactly `BEAST_CUSTOM_ESP_MASTER_PATCH.lua` inside the ZIP so the user can copy -> replace directly.

---

# Goal

Primary goal:

**Make ordinary Biters visible through walls using a custom ESP if necessary.**

User explicitly accepted the custom ESP path and no longer requires native Survivor Sense/X-ray as long as the result works reliably.

Current technical pipeline target:

`live infected AI list -> identity filter -> world position -> native camera transform -> world-to-screen -> unobtrusive marker overlay`

---

# Proven infected AI anchor and identity

## V39 / V40 lineage

The Synsteric "Invisibility to Infected/Biters" code path yielded the important live AI anchor around:

`cmp [rcx+0x22C8], al`

At that execution point:

- `RCX` is a real live infected AI object.

Safe exact signature used in the V40 safe collector lineage:

`38 81 C8 22 00 00 74 18 38 81 60 10 00 00 74 10`

V40R2 safe writer rules that prevented the earlier crash:

- preserve RAX/RDX/R11;
- explicit ring-buffer writer;
- execute original `cmp [rcx+22C8],al` at the end so flags are correct before the original `JE`.

## Identity proof

V40R3 runtime snapshots proved infected identity strings directly from the live AI object.

Repeated examples:

- Biter:
  - `AI+0x23B8 = "Biter"`
  - `AI+0x23F8 = "biter"`
- Viral:
  - `AI+0x23B8 = "Viral"`
  - `AI+0x23F8 = "viral"`

Frozen conclusion:

**RCX from the V39/V40 anchor is a proven live infected AI object.**

For identity filtering prefer `+0x23F8`, with `+0x23B8` as fallback.

---

# Proven / strongest Biter world-position field

## V41 / V41R1

Movement-diff work on the same locked Biter identified two candidates:

- direct: `AI+0x1CC0 / +0x1CC4 / +0x1CC8`
- child: `*(AI+0x208)+0x1C4`

Runtime comparison showed the direct field consistently tracked movement better while the child candidate could stall/freeze.

Frozen working assumption:

**Use `AI+0x1CC0` XYZ as the primary Biter world-position source.**

Do not restart position discovery unless direct runtime evidence invalidates this.

---

# Native Survivor Sense / X-ray experiments — FAILED / DO NOT LOOP

## V42

Same Viral object was captured Sense OFF vs ON. Many stable diff bytes existed, but no single candidate field made a Biter gain native X-ray.

## V44 / V45

Paired Viral/Biter state-transplant work tested grouped candidate state copied from a native-Xray Viral into a Biter.

Shortlisted V44R2 examples included:

- child +0x00A7
- direct AI +0x05C0
- direct AI +0x06FF
- direct AI +0x070B
- direct AI +0x0FEF

V45 grouped transplant result:

**none produced X-ray.**

Frozen conclusion:

Native X-ray is not controlled by a simple copied per-object flag/group in the tested state.

Do not resume V42-V45 style native-state transplant unless a genuinely new native registration/init mechanism is discovered.

---

# Pivot to custom ESP

The user explicitly accepted the custom ESP route.

Known-good ingredients at pivot:

- live infected AI list: proven;
- Biter identity: proven;
- Biter world position `AI+0x1CC0`: strongest/proven working candidate;
- missing piece: camera/view transform + world-to-screen.

---

# MASTER CT architecture

Base artifact lineage:

`BEAST_CUSTOM_ESP_MASTER_R1.CT`

Intent:

- one durable CE master session;
- F1 originally starts/attaches AI core;
- F2 hot reloads the Lua patch;
- future camera/W2S iterations should happen in Lua whenever possible;
- avoid replacing/restarting the whole CT and avoid game relog.

Important historical performance issue:

MASTER R1 originally scanned a 65,536-entry ring every 150 ms. That was too expensive.

R2 SAFE disabled that heavy polling and replaced it with incremental ring processing.

---

# Camera search dead ends / rejected approaches

## R3 camera-lite / memory-region scanning

Large or semi-large `enumMemoryRegions` scanning caused Cheat Engine hangs or severe stalls.

Do not return to broad process memory scanning.

## R4 targeted `.data` delta scan

R4 captured 703 baseline candidates in `gamedll_ph_x64_rwdi.dll` `.data`, but camera-rotation ranking stayed `0`.

Idle camera sway made the baseline-vs-rotated assumption unsuitable.

## R5 inline projection matrix search

R5 tested matrix-like data directly in `.data` and yielded `Projection candidates: 0`, even with multiple Biters visible.

## R6 pointer-chase camera validator

R6 followed `.data` pointers toward heap objects and still returned `Candidates=0`.

Frozen conclusion:

Do not continue blind camera-matrix scanning through `.data` or broad pointer chasing.

---

# Critical process-attach discovery

R7.4 full module dump exposed a major earlier issue:

Cheat Engine Lua/module enumeration was operating on Cheat Engine itself rather than DLTB.

The DLTB process existed separately.

R7.5 auto-attach then proved correct attachment and module resolution:

- DLTB process: `DyingLightGame_TheBeast_x64_rwdi.exe`
- game module: `gamedll_ph_x64_rwdi.dll`

Example session-only addresses from that run:

- EXE base: `0x7FF735540000`
- `gamedll_ph_x64_rwdi.dll` base: `0x7FF8ACFF0000`

Absolute addresses are ASLR/session-specific. Use RVAs/signatures, not those absolute addresses, as persistent identity.

Future patches should ensure the CE process is actually attached to DLTB before scanning/hooking.

---

# Synsteric Headbob anchor / current build mapping

The uploaded Synsteric DLTB Cheat Table 1.1.5 contains a `Disable Headbob` native camera/headbob path.

Old table signature family:

`0F BF 43 ?? F3 0F 10 05`

Once CE was correctly attached to DLTB, the anchor was found and read-only disassembly proved the current build path.

## Current-build anchor

Persistent RVA:

`ANCHOR_RVA = 0x112D772`

Example session absolute address:

`0x7FF8AE13D772`

Relevant exact instructions:

```asm
0x...D76D  test rbx,rbx
0x...D770  je ...D7AA
0x...D772  movsx eax,word ptr [rbx+3E]
0x...D776  movss xmm0,[RIP-relative global]
0x...D77E  movd xmm6,eax
0x...D782  cvtdq2ps xmm6,xmm6
...
0x...D7AA  mov rcx,[rsi+40]
0x...D7AE  mov rax,[rcx]
0x...D7B1  call qword ptr [rax+000005E0]
```

Important crash lesson:

An earlier hook copied the RIP-relative `movss xmm0,[...]` into a code cave and DLTB force-closed.

Frozen rule:

**Never replay that RIP-relative instruction from a relocated cave unless its target is explicitly fixed/re-encoded.**

---

# Proven safe native camera/headbob convergence hook

The safe common-branch hook site is after the headbob branches converge:

Persistent RVA:

`HOOKSITE_RVA = 0x112D7AA`

Original 7 bytes:

`48 8B 4E 40 48 8B 01`

Equivalent instructions:

```asm
mov rcx,[rsi+40]
mov rax,[rcx]
```

These 7 bytes are position-independent and safe to replay in the tested hook design.

## R7.6.5 runtime proof

Artifact lineage:

`BEAST_CUSTOM_ESP_MASTER_R765_CONVERGENCE_READY.zip`

Runtime result:

- hook installed successfully;
- hit count increased continuously;
- exported diagnostic recorded:
  - `INSTALLED=true`
  - `HIT_COUNT=14956`
  - `LAST_RSI=0x22A18A7DD30`
  - `LAST_CHILD40=0x22522072140`

Those absolute pointers are session-specific, but prove the capture path.

## R7.7.1 minimal hook proof

Artifact:

`BEAST_CUSTOM_ESP_MASTER_R771_MINIMAL_HOOK_DIAG_READY.zip`

Exported runtime result:

- `INSTALLED=true`
- `HIT_COUNT=4526`
- `LAST_RSI=0x22A18A7DD30`
- `LAST_CHILD40=0x22522072140`

Frozen conclusion:

**The convergence hook itself is proven stable/live. Do not redesign the camera hook unless direct evidence requires it.**

If future integrated patches show `waiting...`, first suspect Lua symbol/state binding or integration bugs, not the proven hook theory.

---

# R7.6.6 camera object profiler — strongest transform discovery

Profiler reused the proven convergence hook without adding a new game-code hook.

Runtime target map included:

- `RSI`
- `CHILD40 = [RSI+0x40]`
- nearby pointer children.

Strongest transform/matrix-like cluster:

`CHILD40_PTR_008 = [CHILD40+0x8]`

Most important candidate window range:

approximately `+0x1D0` through `+0x260`

Examples from the profiler:

- `+0x220` matrix-like score `68.000`
- `+0x230` matrix-like score `68.000`
- `+0x250` score `61.234`
- `+0x200` score `61.234`

Representative basis-like values changed strongly with yaw:

- ~`0.99353 -> 0.05053 -> 0.02873`
- ~`0.11357 -> -0.99872 -> -0.99959`

This is the strongest camera-transform structure found so far.

Working target for future W2S:

`T = *([RSI+0x40] + 0x8)`

then inspect/interpret transform windows around:

`T + 0x1D0 .. T + 0x260`

Do not resume RAM-wide matrix search before exhausting this proven-local transform cluster.

---

# W2S test result so far

A targeted W2S tester was forced to rank while the AI list was available and successfully saw:

**12 Biters**

This is important proof that the Biter list and camera-side work were both present in the same session at least once.

However the selected candidate was wrong:

- all Biter labels/markers stacked near the upper-right/right side of the screen;
- markers did not correspond correctly to visible Biter positions.

The old fullscreen overlay was also intrusive and effectively blocked normal control until it disappeared/was closed.

Frozen UI rule:

Future visual testing should use:

- short flash overlay, or
- transparent click-through overlay, or
- small preview window,

not a persistent opaque fullscreen overlay.

---

# Integration failures after R7.7.1 — IMPORTANT

Several integrated W2S revisions showed `waiting...` forever even though the camera hook was already proven separately.

Root causes encountered included:

- hot-reload losing old Lua `_G` state while old CE symbols/hooks remained;
- patch saying a hook was "reused" merely because a symbol existed even when the associated Lua state/buffer was dead;
- symbol-name mismatch between writer and reader (`R770_*` vs `R771_*` lineage);
- auto-rebind logic becoming less reliable than the manually installed proven R7.7.1 path.

Do not interpret integrated `waiting...` as evidence that the convergence hook theory failed.

Prefer explicit raw-symbol verification:

- hooksite bytes changed to the expected JMP;
- raw hit counter memory increases;
- raw RSI is nonzero;
- raw `[RSI+40]` is nonzero;
- AI ring/index is independently proven active.

---

# Latest artifact / exact pause point

Latest artifact produced immediately before pause:

`BEAST_CUSTOM_ESP_MASTER_R774_MANUAL_PROVEN_READY.zip`

Version intent:

**R7.7.4 MANUAL PROVEN CORE**

Design choice:

- stop auto-installing/rebinding everything during F2;
- return to the R7.7.1 manual-install behavior that actually produced a rising raw hit counter;
- one manual `FIX CORE NOW` action should establish both camera core and AI core;
- only enable/attempt W2S rank after raw camera hit and Biter count are both live.

Important:

**R7.7.4 has not yet received a user runtime result in this checkpoint.**

The project is intentionally paused before that test.

---

# SP1 next_safe_action

When the user resumes by saying `SP1`:

1. Read actual GitHub HEAD, root `MASTER_STATE.md`, and this `MASTER_STATE_SP1.md` first.
2. Do not revisit native Sense V42-V45 or broad camera RAM scans R3-R6.
3. Treat the infected AI identity anchor and `AI+0x1CC0` position as preserved/proven working inputs.
4. Treat camera anchor RVA `0x112D772` and convergence hook RVA `0x112D7AA` as current-build proven mapping.
5. Treat the 7-byte convergence hook (`48 8B 4E 40 48 8B 01`) as proven live from R7.6.5 and R7.7.1.
6. First runtime action should be testing **R7.7.4 MANUAL PROVEN CORE** exactly once.
7. Require visible proof within 2-3 seconds after manual core activation:
   - raw camera HIT counter rising;
   - raw RSI nonzero;
   - raw `[RSI+40]` nonzero;
   - Biter count > 0 / AI ring active.
8. If camera hit works but Biters stay 0, debug only AI collector integration; do not touch camera hook.
9. If Biters work but camera hit stays 0, compare raw hooksite bytes and install path against R7.7.1; do not redesign the hook until mismatch is identified.
10. Once both are live in the same patch, use only the targeted transform path `[CHILD40+8]` around `+0x1D0..+0x260` for W2S candidate interpretation.
11. Use flash/click-through/small-preview rendering only.
12. Do not use the previously wrong candidate that stacked 12 Biter markers at the upper-right.
13. Rank projection modes against real Biter `AI+0x1CC0` points; test row-major/column-major and camera-world vs view/inverse-view interpretations explicitly.
14. When one candidate visibly tracks a Biter correctly while the camera moves, export/pin:
    - transform pointer path;
    - selected offset;
    - matrix convention;
    - FOV/projection assumptions if any;
    - stable session-independent derivation.
15. Only after visual W2S is proven should the final ESP UI be built (distance/name/filter/cleanup/dead-AI handling).
16. Preserve no-relog workflow whenever possible.

---

# SP1 rejected / do-not-repeat list

- broad `enumMemoryRegions` camera scans;
- `.data` inline matrix guessing as the primary path;
- blind `.data` pointer-chase matrix search;
- native Sense per-object transplant loops;
- relocating the RIP-relative `movss` instruction from anchor `+0x4` without fixing its target;
- persistent opaque fullscreen overlay;
- assuming an existing CE symbol means a live/reusable Lua state;
- auto-rebind chains that overwrite the manually proven convergence hook without raw verification;
- waiting a minute on a `waiting...` state: if raw state is not live in 2-3 seconds, treat it as a bug.

---

# SP1 proof summary

## GREEN / proven

- V39/V40 live infected AI anchor.
- Biter/Viral identity at AI `+0x23B8/+0x23F8`.
- primary Biter world position at AI `+0x1CC0` lineage.
- correct CE attachment to DLTB and correct game module discovery.
- current-build headbob/camera anchor RVA `0x112D772`.
- safe convergence hook RVA `0x112D7AA`.
- R7.6.5 convergence hook hit continuously (`14956` in export).
- R7.7.1 minimal convergence hook hit continuously (`4526` in export).
- live `RSI` and `[RSI+40]` camera-side pointers captured.
- R7.6.6 strong transform cluster at `[CHILD40+8] + ~0x1D0..0x260`.
- Biter list was simultaneously available once with 12 Biters during forced W2S rank.

## Not proven yet

- correct world-to-screen convention / selected transform offset;
- final Biter marker alignment;
- stable final overlay;
- integrated self-contained camera+AI core after hot reload;
- R7.7.4 runtime result.

## Failed / rejected

- V42-V45 native Sense transplant path;
- R3 broad camera scan / CE hang lineage;
- R4-R6 blind matrix/pointer camera resolver lineage;
- wrong W2S candidate that stacked markers upper-right;
- integrated auto-rebind/state-reuse revisions that remained `waiting...`.
