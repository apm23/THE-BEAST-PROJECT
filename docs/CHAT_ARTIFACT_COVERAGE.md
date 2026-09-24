# Chat artifact coverage checklist

This file records which important artifacts from the development chat are preserved in Git as source/reproduction material and which remain local-only by design.

## Portable / preserved in Git

- Exact 1.71E 58-target list: `config/baseline_1.71E_targets.txt`.
- Exact 1.71E per-file size/SHA-256 manifest: `config/baseline_1.71E_manifest.json`.
- 1.71E capture metadata: `config/baseline_1.71E_capture.json`.
- 366 project-relevant archive path index: `config/relevant_file_list_1.71E/part01.txt` ... `part06.txt`.
- Verified local extractor: `tools/extract_targeted_baseline_1.71E.ps1`.
- One-step bootstrap: `tools/BOOTSTRAP_1.71E_USER_SPECIAL45.cmd` + `tools/bootstrap_1.71E_user_special45.ps1`.
- Canonical USER HIGH LOOT SPECIAL45 payload builder: `tools/build_user_special45_payload.py`.
- Canonical USER HIGH LOOT SPECIAL45 reconstruction payload/patch material: `patches/runtime/USER_HIGH_LOOT_SPECIAL45_1.71E/`.
- Runtime NORMAL <-> CO-OP MultiMod switcher source: `tools/runtime_switcher/`.
- Emergency total-clean source: `tools/cleanup/`.
- POC-003 builder source and POC docs/results are retained in their existing project paths.
- Current one-click installer source archival is being added under `tools/oneclick_user_special45/`.

## Local-only by design

The following are intentionally NOT committed because they contain proprietary game data, built modified PAKs, saves, or third-party binaries:

- `DLTB_TARGETS_1.71E.zip` (58 extracted vanilla files).
- Any original extracted vanilla `.scr/.loot/.def` file contents.
- `data0.pak`, `data1.pak`, built `data2.pak`, built `data3.pak`.
- User saves.
- Data Pak Limit Bypass / MultiMod DLL or EXE files.
- Binary ZIP distributions that embed modified/proprietary game definitions.

Portability is provided by exact manifests + local extraction + reproducible project tooling instead.

## Runtime-green local artifacts tracked by hash

See `docs/ARTIFACT_INDEX.md` and `MASTER_STATE.md` for canonical hashes and status of:

- CORPSE SAFE A1+A2.
- GREEN BALANCED.
- USER HIGH LOOT SPECIAL45.
- optional SIBLING BALANCED SPECIAL45.
- USER SPECIAL45 NORMAL/CO-OP mode switcher.
- TOTAL CLEAN tool.

## Failed/rejected artifacts

Failed installers/builds remain documented by name and failure reason in `MASTER_STATE.md` / `docs/ARTIFACT_INDEX.md`. They should not be reconstructed as active install candidates unless explicitly needed for forensic comparison.

## Portability criterion

A fresh machine is considered ready when it can:

1. clone this repository;
2. extract and verify all 58 targets from an owned DLTB 1.71E install with 58 verified / 0 missing / 0 mismatch;
3. rebuild canonical USER HIGH LOOT SPECIAL45 to the expected data2 SHA-256;
4. prepare the runtime switcher without storing proprietary payloads in Git;
5. enter NORMAL or CO-OP MultiMod mode using the frozen switcher logic.
