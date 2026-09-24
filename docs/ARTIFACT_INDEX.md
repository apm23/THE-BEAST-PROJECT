# Local artifact index

This index records important binaries/packages produced during development. The artifacts themselves remain local-only; source, audit metadata, hashes, and reproduction instructions belong in Git.

## Runtime-green lineage

| Artifact | Status | Important SHA-256 |
|---|---|---|
| `DLTB_V3_CORPSE_SAFE_A1_A2.zip` | runtime GREEN structural ancestor | data2 `dc7dc7970088f7a4f3e7c547c0a6fb7229abaadca8a30f3836491e4624015c75` |
| `DLTB_V3_GREEN_BALANCED.zip` | GREEN balance reference | data2 `ecbbbc1ca3725c4507ce6e3f893c5e3438dc882e1a4bd4b69dbff4457812609e` |
| `DLTB_ONECLICK_SIBLING_BALANCED_SPECIAL45.zip` | optional sibling profile | data2 `ab18b545bffbee00ff8ff8ee1e0a9b241bfb2f5864aa88bedc282dab428e771d`; ZIP `4e7013a60c10acadaa98a04af78205333cfc86796572227d99d78ebc3c5311b6` |
| `DLTB_ONECLICK_USER_HIGH_LOOT_SPECIAL45.zip` | canonical user gameplay package | data2 `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`; ZIP `780ce15ce103febee1f9ebd3d35a272c3635e8683f07f404b4f9094b9890429c` |
| `DLTB_USER_SPECIAL45_MODE_SWITCHER.zip` | NORMAL <-> CO-OP MultiMod switcher; runtime proven | ZIP `55f20cdc44dda8ad9c79d0d1671bf302ee7a0b1410adbb9bba36bb02d5ed28e7`; payload data2 same canonical user hash |
| `DLTB_TOTAL_CLEAN_TOOL.zip` | emergency local cleanup/reinstall helper | ZIP `1b1e638217a8e8051ce6f981274eaea2dac2d0a0defc7a558eafade327e73de9` |

## Baseline capture

| Artifact | Status | SHA-256 |
|---|---|---|
| `DLTB_TARGETS_1.71E.zip` | local proprietary 58-file extraction; 0 missing; **never commit** | `09a57b50bffd90f9862b36377384b172e23770787ab086b2a65809a9d63455bb` |

## Known failed / rejected packages

Do not recommend or resurrect these as install candidates:

- `DLTB_A1_A2_A3_V3.zip` — triggered DLC disabled behavior.
- `DLTB_A1_A2_A3_V31_SAFE.zip` — failed.
- `DLTB_EMERGENCY_RECOVER_PRE_V3.zip` — recovery attempt failed.
- aggressive V3 final loot rewrite — corpse `F` prompt disappeared.
- `DLTB_V3_GREEN_VANILLA_RECIPE_OUTPUT_STEP1.zip` — abandoned runtime installer path.
- STEP1 FIXED V2 — `Argument types do not match`.
- STEP1 V3 — duplicate Steam path detection bug.

STEP1 V4 succeeded and established the `data2 = gameplay`, `data3 = output-only vanilla recipe override` architecture that was carried forward.
