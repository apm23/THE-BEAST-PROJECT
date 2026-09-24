# Runtime switcher source

This directory preserves the project-authored source from the runtime-proven `DLTB_USER_SPECIAL45_MODE_SWITCHER.zip`.

The gameplay `data2_payload.pak` is intentionally **not committed**. Expected canonical payload SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

The external Data Pak Limit Bypass / MultiMod DLL/EXE is also not bundled.

Proven modes:

- NORMAL: `ph_ft\source\data2.pak` + `data3.pak`
- CO-OP: `ph_ft\MultiMod\data2.pak` + `data3.pak`, project source copies absent

Runtime result: modded user successfully joined sibling's vanilla world in CO-OP MultiMod mode.

The scripts keep hash detection, save backups, four-slot snapshots, rollback attempts, recipe rebuilding from current official `data0/data1`, and unknown-file STOP behavior.

To execute this source exactly as the proven package, place a canonical `data2_payload.pak` beside the scripts whose SHA-256 is the expected hash above. The repository does not store that PAK; future build tooling should regenerate it from the verified local 1.71E baseline.
