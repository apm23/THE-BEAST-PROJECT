# GH1 Phase C — Native Tier / Exotic / Iconic / Legend Research V1 — 2026-10-02

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

## Phase C objective

Determine the safest native mechanism for the next progression layer before any gameplay mutation:
1. native Exotic rarity / blueprint behavior;
2. whether an actual native weapon rarity named Iconic exists;
3. the real weapon rank domain (especially whether explicit weapon IDs extend beyond r15);
4. how Legend level and New Game Plus modify weapon/player damage;
5. whether post-r15 progression should use native automatic scaling rather than synthetic r16-r300 weapon definitions.

## Existing data evidence

Existing official-data reports already show:
- Color_Exotic exists.
- ColorSet_DefaultExotic and ColorSet_ExoticOnly symbols exist.
- multiple vanilla loot color sets assign non-zero Color_Exotic weights.
- no Color_Iconic symbol was found in the current indexed inventory/loot report.
- textual "iconic" occurrences found so far refer to AI/Volatile attack naming, not a weapon rarity.
- IsAutomaticLegendLevelDamageScaling exists in official scripts.
- ApplyLegendLevelOrNewGamePlusModifiers exists in official scripts/damage definitions.
- LegendPoints rewards and LegendaryWeekly bounty systems exist.

This is preliminary evidence only. Do not yet equate Platinum with Iconic and do not invent an Iconic weapon rarity.

## New read-only scanner

Artifact:
GH1_PHASE_C_NATIVE_TIER_LEGEND_SCANNER_V1.zip

SHA256:
b65f1dfad2d2e4f2985812b4531cea77613c6697e92f3160d44ccfcd8b377cd4

Core Python SHA256:
003d3f4821877ce8702b92db9deafda1807799a55cae27b60c419cc47bf2571b

The scanner is read-only and:
- scans official data0/data1 text scripts;
- compares official vs effective current collectables_ft.scr;
- counts Exotic / Platinum / Iconic rarity symbols;
- parses all official Weapon craftplans using ScaleWithPlayerRank + ItemLevel;
- records blueprint color / tier / NextLevelBlueprintName;
- scans explicit dlc_ft_* weapon _rN IDs and reports max observed rank;
- reports every weapon family with any rank >15;
- counts IsAutomaticLegendLevelDamageScaling and ApplyLegendLevelOrNewGamePlusModifiers;
- captures Legend-related numeric lines for later progression analysis;
- outputs:
  - Documents/GH1_PHASE_C_NATIVE_TIER_LEGEND_SCAN_V1.json
  - Documents/GH1_PHASE_C_NATIVE_TIER_LEGEND_SCAN_V1.txt

Synthetic parser self-test:
PASS — craftplan tiers, Exotic/Iconic symbols, weapon ranks and Legend symbols.

## Safety decision gate

Until live scan is returned:
- DO NOT create r16-r300 weapon families.
- DO NOT create a Color_Iconic or claim Platinum == Iconic.
- DO NOT modify Phase B Broad loot.
- DO NOT reuse the rejected temporary CraftPart Ascension carrier.
- Prefer a native scaling path if official data proves Legend progression is runtime scaling rather than item-rank expansion.

## Next safe action

Run GH1_PHASE_C_NATIVE_TIER_LEGEND_SCANNER_V1 and inspect the generated JSON/TXT.

Decision after scan:
- if official max weapon rank is r15 and no weapon ranks >15 exist, freeze explicit weapon rank domain at 1-15;
- if native Exotic symbols/craftplan patterns are confirmed, prototype Exotic progression using that native structure;
- if no native weapon Iconic rarity symbol exists, treat "Iconic" as a project label only unless a separate native mechanism is found;
- map Legend/NG+ automatic scaling before any post-r15 progression mutation.
