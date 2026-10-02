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


## Actual Exotic Workbench Scanner V1 live result

User returned both scanner outputs from the installed live stack.

Live scan:
- effective collectables source: data4.pak
- official weapon blueprints: 150
- current weapon blueprints: 414
- native T4 blueprints: 29 across 29 families
- native T4 blocks using Color_Exotic: 21
- native T4 blocks using Color_Platinum: 0
- generated GH1 families without T4: 88

Key structural result:
- every scanned native Color_Exotic T4 blueprint omits ItemLevel;
- representative native Exotic firearm T4 recipe pattern:
  - Craft_Scrap 35
  - Craft_wiring 12
  - Craft_Leather 12
  - Craft_Firearm_Scrap_FT 6
- representative native Exotic firearm T4 block uses:
  - ItemType(ItemType_CraftPlan)
  - CraftplanType("Weapon")
  - Color(Color_Exotic)
  - ScaleWithPlayerRank("<family>_r")
  - HudIcon("blueprint_b")
  - no NextLevelBlueprintName
  - no ItemLevel
  - GameVersion(9)
- not every T4 is Exotic: 8 of 29 native T4 entries remain Color_Orange. Therefore T4 suffix alone is not a rarity guarantee.

Generated GH1 chains are clean T1/T2/T3:
- T1: Color_Blue + ItemLevel(1,3) + next T2
- T2: Color_Violet + ItemLevel(2,3) + next T3
- T3: Color_Orange + ItemLevel(3,3) + no next
- 88 generated families currently stop here.

This confirms the correct POC question is whether extending a generated T1/T2/T3 upgrade chain to a native-style standalone Color_Exotic T4 is accepted by the workbench runtime.

## Exotic POC1 V1

Artifact:
GH1_PHASE_C_EXOTIC_POC1_V1.zip

Package SHA256:
b5d24de1d504a5f663b9901a4fc7c642af8bbe26accc67844d4a4c9a3879733d

Core Python SHA256:
b2bb5923914dbc0e05ac137bab6cfc7914015b8f84cdf38123d11e6c1f0a23d7

Repo source:
tools/tbp_phase_c_exotic_poc1.py

Repo source commit:
c308d28fe2cbfafb2fa3c7082e84b26e2f494342

POC target:
dlc_ft_firearm_pistol_b_legendary_r

Why this target:
- classification is generated;
- it already belongs to the Phase B 137-family proven pair universe;
- generated chain is exactly T1/T2/T3 Blue/Violet/Orange;
- it has no T4 in the live scan;
- firearm native Exotic T4 recipe structure is well represented in official data.

POC mutation only:
- T1 ItemLevel(1,3) -> ItemLevel(1,4)
- T2 ItemLevel(2,3) -> ItemLevel(2,4)
- T3 ItemLevel(3,3) -> ItemLevel(3,4)
- T3 gains NextLevelBlueprintName(Craftplan_GH1_dlc_ft_firearm_pistol_b_legendary_T4_Blueprint)
- new T4 blueprint:
  - Color(Color_Exotic)
  - same ScaleWithPlayerRank family
  - native firearm Exotic recipe 35/12/12/6
  - no ItemLevel
  - no further NextLevelBlueprintName
  - GameVersion(9)

Installer safety:
- reads the current effective collectables dynamically;
- writes a new highest dataN.pak;
- package contains only collectables_ft.scr plus an exact POC marker;
- does not include or modify loot pools or loot sets;
- does not touch LootedObject topology;
- does not touch save/DLC/player_variables/stash/inventory versioning;
- uninstall removes only the PAK containing the exact POC marker.

Synthetic self-test:
PASS — generated T1/T2/T3 -> native-style Exotic T4 chain; loot untouched.

## Current next runtime proof

Install Exotic POC1 V1 and test at the workbench.

Required observations:
1. target T3 blueprint offers another upgrade;
2. upgraded blueprint becomes T4;
3. crafted/upgraded target weapon is Exotic;
4. weapon level still follows current native Legend/workbench scaling;
5. after save/reload, Exotic rarity and resulting weapon stats persist.

Until these observations pass:
- Exotic generated-family support is POC only, not PROVEN;
- do not mass-expand T4 to all 88 generated families.
