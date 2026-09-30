# Weapon + Outfit Dismantle Cleanup Collector

Status: **read-only collector only**. This tool does not install a gameplay patch.

## Goal

Build an exact inventory-definition map before extending G1/G1.1 cleanup behavior:

- catalogue every weapon-like `Item(...)` definition visible in the owned 1.71E archives/current mod layers;
- record `DismantleResult`, `CanDrop`, `IsShareable`, category, inheritance (`use(...)`), UID and other patch-relevant fields;
- catalogue every `CategoryType_OutfitPart` definition;
- identify likely Vanguard / Night Sovereign carrier definitions;
- flag weapons with no explicit usable dismantle route;
- flag outfits that do not already follow the native `DismantleResult("empty")` removal pattern.

## Safety contract

The collector is deliberately separate from the gameplay patch.

It:

- reads `data0.pak`, `data1.pak`, and any currently present `source` / `MultiMod` `data2`/`data3`;
- extracts inventory scripts only to `local_research/`;
- creates metadata reports/CSV/JSON and a small upload ZIP;
- does **not** write to the game folder;
- does **not** touch saves;
- does **not** touch inventory/save versioning;
- does **not** delete, reorder, or rename `Item` definitions.

The generated upload ZIP excludes raw game scripts. Temporary local extracts are deleted after a successful scan.

## Run

From a cloned THE-BEAST-PROJECT repository on the DLTB machine:

```bat
tools\COLLECT_WEAPON_OUTFIT_DISMANTLE_1.71E.cmd
```

The collector auto-detects the Steam installation. If needed:

```bat
tools\COLLECT_WEAPON_OUTFIT_DISMANTLE_1.71E.cmd -GameDir "D:\SteamLibrary\steamapps\common\Dying Light The Beast"
```

Upload the generated:

`DLTB_WEAPON_OUTFIT_DISMANTLE_RESULT_YYYYMMDD_HHMMSS.zip`

## Output

The upload ZIP contains generated metadata only:

- `_WEAPON_OUTFIT_DISMANTLE_REPORT.txt`
- `_WEAPON_OUTFIT_EFFECTIVE.csv`
- `_WEAPON_OUTFIT_ALL_OCCURRENCES.csv`
- `_WEAPON_OUTFIT_SNAPSHOT.json`
- `_ARCHIVE_HASHES.txt`
- `_READ_ME_FIRST.txt`

The collector marks a likely effective definition using the highest discovered PAK layer for each logical script path. That is an audit heuristic, not engine-runtime proof.

## Intended next patch

After collector review:

1. preserve every existing G1.1 item identity and registry order;
2. keep existing valid native weapon dismantle families;
3. patch only weapon definitions that actually need an explicit dismantle route, choosing the native family appropriate to weapon class/tier;
4. for the six Night Sovereign/Vanguard outfit carriers, prefer the native outfit removal pattern (`DismantleResult("empty")`) rather than world-drop cleanup;
5. keep the change isolated to inventory definitions;
6. build with exact source hashes, back up save, and run the standard inventory/attack/corpse-`F`/save-reload smoke test before calling it GREEN.

No Alpha3/Alpha4 registry-parity behavior is part of this work.
