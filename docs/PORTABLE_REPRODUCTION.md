# Portable reproduction / local baseline contract

The repository is intentionally **source/tooling only**. It does not redistribute Techland game data, extracted vanilla scripts, `data*.pak`, saves, DLLs, EXEs, or third-party loader binaries.

The original project session captured a clean Dying Light: The Beast **1.71E** installation with `data0.pak` + `data1.pak`. A targeted set of **58 files** was extracted successfully with **0 missing**. The exact path, size, and SHA-256 fingerprint of every captured file is committed in:

- `config/baseline_1.71E_targets.txt`
- `config/baseline_1.71E_manifest.json`
- `config/baseline_1.71E_capture.json`

The local reference ZIP from the original session had SHA-256:

`09a57b50bffd90f9862b36377384b172e23770787ab086b2a65809a9d63455bb`

That ZIP is **not** committed because it contains proprietary extracted game content.

## Fast path — rebuild the current proven mod on a fresh machine

Requirements:

1. An owned/local Dying Light: The Beast installation matching build 1.71E.
2. Clone this repository.
3. Python 3.
4. 7-Zip recommended; Windows `tar.exe` is a fallback if it can read the PAK.

From the repo, run:

`tools\BOOTSTRAP_1.71E_USER_SPECIAL45.cmd`

The bootstrap performs:

1. exact 58-file baseline extraction + hash/size verification;
2. exact USER HIGH LOOT SPECIAL45 `data2_payload.pak` reconstruction;
3. byte/hash verification against the canonical payload;
4. copy of that verified payload into `tools/runtime_switcher/data2_payload.pak` so the proven NORMAL/CO-OP switcher source is ready.

Canonical rebuilt payload SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

The reconstruction has been tested against the original canonical payload and produced **byte-for-byte identical output**.

## Recreate only the 58-file baseline

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\extract_targeted_baseline_1.71E.ps1
```

The script auto-detects Steam libraries. If needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\extract_targeted_baseline_1.71E.ps1 -GameDir "C:\Program Files (x86)\Steam\steamapps\common\Dying Light The Beast"
```

Output:

`local_baseline/1.71E/`

The extractor validates each target against the captured 1.71E SHA-256 + byte size and writes:

`local_baseline/1.71E/_VERIFY_REPORT.json`

Expected exact result:

- targets: 58
- verified: 58
- missing: 0
- mismatch: 0

`local_baseline/` is gitignored.

## Exact payload rebuild internals

Builder:

`tools/build_user_special45_payload.py`

Patch source:

`patches/runtime/USER_HIGH_LOOT_SPECIAL45_1.71E/`

Only compact project delta instructions are committed. The builder verifies and patches these three baseline definitions:

- `scripts/inventory/inventory_ranged.scr`
  - baseline SHA-256 `610622dae7450d36a873ea630dbf9fac2757e359fa4d159b23305a0590b82b20`
  - canonical final SHA-256 `8bf5e4d097972ed9075f6105efe4e5fb533d44ecd5f3dd39cc44fb5bd210f745`
- `scripts/inventory/loot/lootpools_ft.loot`
  - baseline SHA-256 `fac968e396e185888f20cdfc20543f4a492d10f21f5dde0c8f8b2c9c054a9f98`
  - canonical final SHA-256 `46fe4e2c3c63e68fda99c80c1982689cbd874f16c1c173e2fa6643501be8635e`
- `scripts/inventory/loot/lootsets_ft.loot`
  - baseline SHA-256 `9addc1fbfb35b56c8be9928307208b12f3f0672cf303affdba661a4193d6410a`
  - canonical final SHA-256 `b6f2f78ab4a2c0dcf1a1feddd2129de4c60eedb4900c894e628c91292669c308`

Manual build command after baseline extraction:

```powershell
python .\tools\build_user_special45_payload.py --prepare-switcher
```

Default build output:

`local_build/USER_HIGH_LOOT_SPECIAL45/data2_payload.pak`

`--prepare-switcher` also copies the verified payload to:

`tools/runtime_switcher/data2_payload.pak`

PAK files remain gitignored.

## Archive metadata captured from the original session

The original baseline scanner recorded:

- `AllPathCount=19727`
- `RelevantPathCount=366`
- `data0.pak,data1.pak`

The exact 366 project-relevant archive-path records are committed as six text parts under:

`config/relevant_file_list_1.71E/`

Concatenate `part01.txt` through `part06.txt` in lexical order to reconstruct the original 366-line list. This is path metadata only; no vanilla file content is stored there.

## Runtime switcher source

Project-authored switcher source is committed under:

`tools/runtime_switcher/`

It preserves the runtime-proven NORMAL <-> CO-OP MultiMod behavior without committing the gameplay PAK or any third-party loader binary.

After bootstrap, use:

- `tools\runtime_switcher\1_SWITCH_TO_COOP_MULTIMOD.cmd`
- `tools\runtime_switcher\2_SWITCH_BACK_NORMAL_PROVEN.cmd`
- `tools\runtime_switcher\3_CHECK_CURRENT_MODE.cmd`
- `tools\runtime_switcher\4_DISABLE_OUR_MOD.cmd`

The exact tested CO-OP milestone remains: modded user successfully joined sibling's vanilla world while the project payload was loaded from MultiMod.

## Other archived project-authored tooling

Emergency cleanup source:

`tools/cleanup/`

Artifact/hash history:

`docs/ARTIFACT_INDEX.md`

## Safety invariant

Never make the repository "portable" by committing the original 58 extracted files or a built `data2.pak`/`data3.pak`. Portability is achieved by **exact manifest + local extraction + project delta patches + deterministic rebuild tooling**.
