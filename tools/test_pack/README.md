# DLTB SPECIAL45 A/B Test Pack

Purpose: compare the exact proven USER HIGH LOOT SPECIAL45 control against the new ordinary-Biter resource-parity candidate from a known clean mod state.

## What CLEAN means here

This pack does **not** delete the game or saves.

Before either install, it:

- keeps official `ph_ft/source/data0.pak` and `data1.pak`;
- backs up saves;
- quarantines every live `dataN.pak` except official data0/data1 under `ph_ft/_THE_BEAST_PROJECT_BACKUPS/`;
- quarantines the complete live `ph_ft/MultiMod` folder;
- quarantines `ph_ft/work/bin/x64/CustomPak.ini` so MultiMod routing is disabled;
- quarantines known THE BEAST PROJECT state markers;
- verifies there is no remaining live non-official `dataN.pak` before continuing.

This is intentionally different from the historical `DLTB_TOTAL_CLEAN.ps1`, which can delete the whole local game/save/cache installation. The A/B pack only cleans live mod routing/data while preserving the installed game and save data.

## Requirements

- Dying Light: The Beast **1.71E** installed through the user's own Steam installation.
- Python 3.
- 7-Zip recommended; Windows `tar.exe` is accepted if it can read the PAK.
- Game must be closed.

The pack contains no proprietary game PAK contents. It reconstructs both payloads from the user's verified local 1.71E archives.

## Buttons

### `1_CLEAN_ALL_MODS_FOR_TEST.cmd`

Manual clean/quarantine only. Safe first step if you want to inspect the game state before installing either side of the A/B test.

### `2_INSTALL_NEW_BITER_RESOURCE_TEST.cmd`

Automatically performs clean again, verifies/extracts the exact 1.71E baseline, reconstructs canonical SPECIAL45, then applies the Biter resource-parity delta and installs it in NORMAL source mode.

Candidate rules:

- parent must reconstruct to exact SPECIAL45 SHA-256 `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657` before candidate patching;
- `lootpools_ft.loot` remains byte-identical to SPECIAL45;
- only `lootsets_ft.loot` Biter resource sub-pools are changed;
- listed normal crafting resources receive internal weight `5.0`, equal to Scrap;
- Scrap quantity remains `40-55`;
- non-Scrap crafting resource quantity remains `33-50`.

### `3_RESTORE_PROVEN_SPECIAL45.cmd`

Automatically cleans the candidate/other live mod data again, rebuilds the exact proven SPECIAL45 payload, requires SHA-256 `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`, rebuilds recipe `data3`, and installs the proven control in NORMAL source mode.

### `4_CHECK_TEST_STATUS.cmd`

Shows current live `data2/data3`, MultiMod/CustomPak state, non-official live PAK count, and A/B state marker.

## Recommended runtime comparison

1. Run `1_CLEAN_ALL_MODS_FOR_TEST.cmd` once and confirm PASS.
2. Run `2_INSTALL_NEW_BITER_RESOURCE_TEST.cmd`.
3. Test ordinary Biters: corpse `F`, Battery, Electrical Parts, Pigments, Oxidizer, Wiring, etc.; quantity ranges; DLC popup; save/reload.
4. Record the result.
5. Close the game.
6. Run `3_RESTORE_PROVEN_SPECIAL45.cmd`.
7. Repeat the same route/test with the proven control.
8. Compare results.

Do not promote the candidate to canonical/proven until NORMAL runtime tests pass. COOP_MULTIMOD should be tested only after the isolated NORMAL A/B test passes.
