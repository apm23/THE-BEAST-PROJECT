# GH1 Phase C — Exotic Focus / Legend Deferred — 2026-10-02

## Entry condition

Phase B weapon + matching blueprint loot is FINAL PROVEN.

Locked Phase B evidence:
- 137/137 paired weapon families reachable
- 49 native blueprint families
- 88 generated blueprint families
- 2041/2041 valid pair bundles reachable
- 32/32 infected NORMAL/PERMA Broad routes
- zero unreachable families
- zero coverage issues
- runtime broad variety proven
- generated blueprint acquisition runtime proven

Do not reopen the rejected local loot architecture. Global tbp_* remains frozen baseline.

## User runtime observation — Legend handling

User reports an old weapon could be upgraded manually at the workbench up to the user's current Legend level 29.

Interpretation for project planning:
- treat Legend-level weapon scaling as already handled by the game's native/workbench system unless future evidence contradicts it;
- DO NOT build synthetic r16-r300 weapon families;
- DO NOT build a competing custom Legend scaling layer now;
- Legend progression is DEFERRED/FROZEN while Exotic is solved.

This runtime observation is not yet a formal data proof of every Legend behavior, but it is strong enough to change project priority.

## Phase C narrowed objective

Focus only on native Exotic progression:
1. identify exact native T4/workbench blueprint structure;
2. determine how native T4 relates to Exotic output;
3. extend generated GH1 weapon blueprint families through the same native-safe path;
4. create a small one-family POC first;
5. user manually upgrades the POC at the workbench and verifies rarity/result/persistence;
6. only after runtime GREEN, expand to all eligible generated families.

## Existing evidence

Official-data reports show:
- Color_Exotic exists.
- ColorSet_DefaultExotic and ColorSet_ExoticOnly exist.
- current/proven loot already uses ColorSet_ExoticOnly.
- a native Legend reward gives both:
  - dlc_ft_WPN_1HB_STK_T_suspect_r15
  - Craftplan_dlc_ft_WPN_1HB_STK_T_suspect_T4_Blueprint
  and marks IncludesBlueprint().
- current Phase B scan classifies dlc_ft_wpn_1hb_stk_t_suspect_r as native and selects the T4 blueprint for that family.
- no Color_Iconic weapon-rarity symbol has been proven.

Important inference:
T4 is now the highest-priority native workbench reference for Exotic research. Do not assume the T4 suffix alone means Exotic until the exact T4 block is extracted from live official collectables.

## New read-only Exotic scanner

Artifact:
GH1_PHASE_C_EXOTIC_WORKBENCH_SCANNER_V1.zip

Package SHA256:
63214b45c645c7027015fa7f1627ef2ee848f3eed0c8c96acebaaa482b162562

Core Python SHA256:
bb8690f912d03c7866bd0670b11bedef30d6a8285d24d946c8ed98b5047ad155

Purpose:
- extract all native T4 weapon blueprint blocks from official data0/data1 collectables_ft.scr;
- report ScaleWithPlayerRank, ItemLevel, Color, requirements, NextLevelBlueprintName, HudIcon and LinkedDocket;
- compare native T4 families to current generated GH1 blueprint families;
- identify generated families that currently stop below T4;
- make the next POC data-driven rather than guessed.

Outputs:
- Documents/GH1_PHASE_C_EXOTIC_WORKBENCH_SCAN_V1.json
- Documents/GH1_PHASE_C_EXOTIC_WORKBENCH_SCAN_V1.txt

Synthetic parser self-test:
PASS.

## Safety locks

- Phase B Broad loot is frozen.
- Legend custom scaling is deferred.
- No r16-r300 definitions.
- No custom Color_Iconic.
- No temporary CraftPart Ascension carrier.
- No guessed T4 mutation.
- First Exotic mutation must be one-family POC based on an actual extracted native T4 structure.

## Next safe action

Run GH1_PHASE_C_EXOTIC_WORKBENCH_SCANNER_V1.

After its JSON/TXT are returned:
- choose one generated family with a proven T1/T2/T3 chain;
- build a minimal T4/Exotic POC only for that family;
- do not change its Phase B loot pairing unless required;
- user upgrades it manually at workbench;
- verify Exotic rarity/output and save/reload behavior;
- if GREEN, expand T4/Exotic support to the full generated family set.
