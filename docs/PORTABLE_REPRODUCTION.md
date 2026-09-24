# Portable reproduction / local baseline contract

The repository is intentionally **source/tooling only**. It does not redistribute Techland game data, extracted vanilla scripts, `data*.pak`, saves, DLLs, EXEs, or third-party loader binaries.

The original project session captured a clean Dying Light: The Beast **1.71E** installation with `data0.pak` + `data1.pak`. A targeted set of **58 files** was extracted successfully with **0 missing**. The exact path, size, and SHA-256 fingerprint of every captured file is committed in:

- `config/baseline_1.71E_targets.txt`
- `config/baseline_1.71E_manifest.json`

The local reference ZIP from the original session had SHA-256:

`09a57b50bffd90f9862b36377384b172e23770787ab086b2a65809a9d63455bb`

That ZIP is **not** committed because it contains proprietary extracted game content.

## Recreate the 58-file baseline on any Windows machine

Requirements:

1. An owned/local Dying Light: The Beast installation matching build 1.71E.
2. 7-Zip recommended. Windows `tar.exe` is used as fallback if it can read the PAK.
3. Clone this repository.

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

## Archive metadata captured from the original session

The original baseline scanner recorded:

- `AllPathCount=19727`
- `RelevantPathCount=366`
- `data0.pak,data1.pak`

The 366 project-relevant path list is committed as `config/relevant_file_list_1.71E.txt` so future work can search likely game definitions without redistributing their contents.

## Current runtime tooling source

Project-authored switcher source is committed under `tools/runtime_switcher/`. It preserves the proven NORMAL <-> CO-OP MultiMod logic without committing the gameplay `data2_payload.pak` or any third-party loader binary.

The canonical USER HIGH LOOT SPECIAL45 payload SHA-256 remains:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Because the gameplay PAK contains modified game definitions, it remains local-only. Future portable build tooling should regenerate it from the verified local 1.71E baseline and project-authored patch logic rather than storing the PAK in Git.

## Safety invariant

Never make the repository "portable" by committing the original 58 extracted files or a built `data2.pak`/`data3.pak`. Portability is achieved by **manifest + local extraction + project patch/build tooling**.
