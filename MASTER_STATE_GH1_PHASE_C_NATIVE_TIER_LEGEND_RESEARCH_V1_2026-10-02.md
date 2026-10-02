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


## Exotic POC1 runtime result — HARD REJECTED

User runtime test produced two independent failures:

1. On game load the UI displayed:
   DLC ITEMS DISABLED
   "DLC no longer detected. Some items have been removed from your inventory. Please reinstall or enable DLC for content."

2. Workbench result:
   - T3 blueprints did not gain a usable upgrade path to Exotic.
   - user reports all tested T3 blueprints still could not become Exotic.

Therefore POC1 architecture is HARD REJECTED.

Immediate safety action:
- close the game;
- run 2_UNINSTALL_EXOTIC_POC1.cmd;
- relaunch only after the POC marker PAK is gone;
- if DLC-owned inventory remains missing after DLC detection returns, use a pre-POC save backup if available.

Do not reuse POC1's T1/T2/T3 ItemLevel max-tier rewrite or T3 -> T4 NextLevelBlueprintName approach.

## Important packaging defect discovered after runtime failure

POC1 wrote its dataN.pak with Python zipfile ZIP_STORED and default ZipInfo metadata.

The previously runtime-proven Phase B overlays use a different package writer:
- ZIP_DEFLATED, compresslevel=9;
- deterministic ZipInfo timestamp;
- external_attr=0x01800000;
- create_system=3.

Because the POC1 PAK format differs from the proven overlay writer, packaging is now a primary suspected contributor to the DLC-disabled failure. This is not yet isolated as the only cause; the T3->T4 semantic mutation also failed independently.

Future PAK-writing POCs MUST reuse the proven Phase B write_overlay packaging pattern byte-structure conventions rather than the ad-hoc ZIP_STORED writer.

## Corrected Exotic model after POC1

The live scanner already showed:
- 21 native T4 blueprints are Color_Exotic;
- native Exotic T4 entries have no ItemLevel and no NextLevelBlueprintName;
- not every T4 is Exotic;
- official data contains at least one progression reward that grants an r15 weapon together with its T4 blueprint using IncludesBlueprint().

Runtime POC1 now adds the decisive negative result:
- making T3 point to T4 does not create the desired native Exotic upgrade path.

Current working hypothesis:
native Exotic T4 is a standalone blueprint/unlock/reward tier, not a normal continuation of the T1->T2->T3 upgrade chain.

## Next safe action

POC2 must be structurally different:
- do not modify T1/T2/T3 ItemLevel;
- do not attach T4 through NextLevelBlueprintName;
- add one standalone generated Color_Exotic T4 blueprint only;
- acquire/deliver that T4 through a separate native-style blueprint reward/drop mechanism for testing;
- package the overlay with the exact proven Phase B ZIP_DEFLATED writer;
- keep Phase B Broad route topology frozen;
- first test only whether possession of the standalone T4 blueprint can craft the same generated weapon as Exotic and whether that survives save/reload.

Do not mass-expand to 88 generated families until standalone T4 acquisition/crafting is runtime GREEN.


## DLC recovery package after POC1 rejection

User uninstalled Exotic POC1 and requested a safe way to re-enable legitimate DLC detection.

Recovery artifact:
GH1_DLC_RECOVERY_VANILLA_CYCLE_V1.zip

SHA256:
5e2d201c6fbfa949ac5291d24d170c9f87b420f694625beaa47ebd069d595ce0

Repo source:
tools/GH1_DLC_RECOVERY.ps1

Repo commit:
f312b631f9a7aa2cbd9729157ef09df516f9940d

Recovery design:
- does NOT spoof or modify Steam/DLC entitlement;
- does NOT edit save data;
- backs up current Steam save from app 3008130 before mutation;
- temporarily quarantines exact active source data2+.pak files;
- temporarily quarantines MultiMod data*.pak files;
- temporarily quarantines CustomPak.ini;
- leaves official data0.pak and data1.pak untouched;
- user boots the game once in clean vanilla state to allow normal DLC detection;
- restore command returns every quarantined mod file to its exact original path;
- restore verifies SHA256 before completing;
- save-backup finder lists prior project backups but never auto-restores one.

Runtime sequence:
1. close game;
2. run 1_ENTER_VANILLA_DLC_RECOVERY.cmd;
3. launch game once clean and check DLC detection;
4. close game;
5. run 2_RESTORE_PHASEB_STACK.cmd;
6. if DLC detection is restored but inventory DLC items remain missing, enumerate pre-existing save backups before any manual save restore.

This is now the preferred recovery path for the POC1 DLC-disabled incident.


## Project mode change — OFFLINE BUILD MODE

User elected to postpone game/DLC recovery and runtime testing until the mod is otherwise complete.

From this point:
- Phase B proven stack remains frozen.
- Do not ask the user to repeatedly install/test intermediate POCs.
- Continue research, scanners, builders, static validation, packaging, and final integration offline.
- Any feature not runtime-tested after the DLC incident must be labeled CANDIDATE / UNPROVEN, never PROVEN.
- Avoid save-sensitive, entitlement-sensitive, DLC-sensitive, inventory-versioning, stash, player_variables, or LootedObject topology changes.
- No runtime package should be installed on the user's current game until the final clean reinstall/verify cycle.
- Exotic development continues as standalone-T4 research/build only; do not reuse the rejected T3->T4 chain.
- Final validation plan:
  1. clean reinstall / Steam verify;
  2. confirm DLC detection is healthy;
  3. install one integrated final candidate;
  4. run one consolidated runtime test matrix;
  5. only then promote remaining candidate features to PROVEN.

This mode intentionally trades early runtime feedback for fewer risky install cycles.


## Offline Exotic candidate — 127/137 coverage

Artifact:
GH1_PHASE_C_EXOTIC_127_OFFLINE_CANDIDATE_V1.zip

Package SHA256:
4fca53bcbe10a0e485785d24adc61e9a076893ad57cff168cd17578e6e733817

Core Python SHA256:
c871d2f0b495dd2dea323b689591facfe54579fcd3051fb89ffda59bdd70a7cd

Manifest SHA256:
fcd87260e81e085dc630fcd00d88d645d6c6a5c0b6503a3a4b188c6303dbb8b5

Status:
CANDIDATE / UNPROVEN — OFFLINE BUILD MODE. Do not install until final clean reinstall / Steam verify cycle.

### Important refinement from live Phase B + Exotic scan data

The Phase B live coverage report and Exotic scanner were cross-mapped.

137-family Phase B universe splits into:
- 21 families already using a native Color_Exotic T4 blueprint;
- 106 families with a normal T1 -> T2 -> T3 chain and no T4;
- 7 families with a native T4 that is Color_Orange, not Exotic;
- 3 special firearm families with no normal T1/T2/T3 ScaleWithPlayerRank chain.

The 21 native Exotic families already use their native T4 as the Phase B paired blueprint. They therefore require no mutation.

The safe candidate target is only the 106 normal tier-chain families.

### Candidate behavior

For each of the 106 T1/T2/T3 families:
- leave T1/T2/T3 definitions byte-identical;
- create one standalone native-style T4 blueprint;
- T4 uses Color(Color_Exotic);
- T4 uses the same ScaleWithPlayerRank family;
- T4 has no ItemLevel;
- T4 has no NextLevelBlueprintName;
- firearm recipe follows native Exotic firearm pattern 35 Scrap / 12 Wiring / 12 Leather / 6 Firearm Scrap;
- melee recipe follows native Exotic melee pattern 50 Scrap / 20 Wiring / 20 Leather / 12 Weights;
- add the T4 blueprint as a third item to the same existing Phase B weapon+matching-blueprint ItemBundle.

Exact bundle mutations:
1576 existing Phase B pair bundles.

This does not change:
- default.loot
- tbp_lootpools_global_v1.loot
- tbp_lootsets_global_v1.loot
- any LootedObject topology
- any route weight
- resource/charm/Night Sovereign routes
- T1/T2/T3 definitions
- stash/inventory versioning/player_variables
- save format

Candidate Exotic coverage if the standalone T4 runtime hypothesis is GREEN:
127 / 137 families.

### Deliberately deferred edge families

Native Orange T4 — do not rewrite without separate proof:
- dlc_ft_firearm_revolver_1stanniversary_r
- dlc_ft_firearm_rifle_1stanniversary_r
- dlc_ft_firearm_rifle_l_r
- dlc_ft_firearm_shotgun_1stanniversary_r
- dlc_ft_wpn_15hs_18_r
- dlc_ft_wpn_1hb_stk_z_1stanniversary_r
- dlc_ft_wpn_1hs_mach_27_r

No normal T1/T2/T3 tier chain — do not invent a tier chain:
- dlc_ft_firearm_flamethrower_r
- dlc_ft_firearm_grenadelauncher_r
- dlc_ft_firearm_sawbladelauncher_r

### Static validation

SELFTEST PASS:
- 137 Phase B family manifest validated
- 2041 Phase B pair bundle manifest validated
- 21 native Exotic families reused
- 106 standalone Exotic T4 definitions generated
- 1576 exact existing pair bundles enriched
- 10 edge families untouched
- T1/T2/T3 byte-identical validation
- Phase B route topology untouched
- package ZIP integrity PASS

The runtime package writer uses the proven overlay pattern:
- ZIP_DEFLATED
- compresslevel 9
- deterministic ZipInfo timestamp
- external_attr 0x01800000
- create_system 3

This explicitly avoids the ad-hoc ZIP_STORED packaging used by rejected POC1.

### Final runtime gate

After final clean reinstall / Steam verify:
1. confirm DLC is detected with no warning;
2. restore/install proven Phase B Broad Final V2;
3. run candidate self-test;
4. install Exotic 127 candidate;
5. verify generated firearm and melee corpse pair bundles grant standalone T4 blueprint;
6. verify T4 crafts the same family as Exotic;
7. verify native Legend/workbench level scaling remains normal;
8. save/reload and confirm Exotic rarity/stats persist;
9. only then promote Exotic 127 candidate to PROVEN.

Do not call the 106 custom T4 families PROVEN before that runtime gate.


## Exotic All137 Offline Candidate V2 — full family coverage candidate

Artifact:
GH1_PHASE_C_EXOTIC_ALL137_OFFLINE_CANDIDATE_V2.zip

Package SHA256:
d6e2877128b3c1b292c0ed7f0224603c5810317c99ea05ff4a3cdb105f376d13

Core Python SHA256:
3c8f4a5e8f04af5a3646a5c686e0cd90c53d39f8a9940fcd3c3d95c0bfd78d51

Manifest SHA256:
32f53b43604e16408393225ea51f95bcaf31d6cf025a5314cbfbb234316f4530

Status:
CANDIDATE / UNPROVEN — OFFLINE BUILD MODE. This supersedes the 127/137 candidate as the primary final-test candidate. Keep 127/137 V1 only as a conservative fallback.

### Edge-family audit breakthrough

The three special launcher blueprints that do not use ItemLevel still use native ScaleWithPlayerRank:
- Craftplan_FlameThrower_FT -> dlc_ft_firearm_flamethrower_r
- Craftplan_GrenadeLauncher_FT -> dlc_ft_firearm_grenadelauncher_r
- Craftplan_SawbladeLauncher_FT -> dlc_ft_firearm_sawbladelauncher_r

Therefore they can be treated as standalone scalable weapon blueprint templates rather than requiring an invented T1/T2/T3 chain.

The seven native Orange T4 edge families also do not need their native T4 rewritten. A separate GH1 Exotic sibling blueprint can coexist while the original native Orange T4 remains byte-identical.

### Full 137-family candidate model

137 Phase B weapon families now map as:
- 21 native Color_Exotic T4 families: reuse exact native Exotic blueprint.
- 106 ordinary T1/T2/T3 families: create standalone GH1 Exotic sibling from the existing family identity.
- 7 native Color_Orange T4 families: preserve native Orange T4 and create separate standalone GH1 Exotic sibling.
- 3 special standalone Orange launcher families: preserve original blueprint and create separate standalone GH1 Exotic sibling.

Custom Exotic siblings created:
116.

Pair bundles enriched:
1726.

Native Exotic bundles already correct and reused:
315 bundles across 21 families.

Total Phase B pair bundle universe remains:
2041.

Candidate Exotic blueprint coverage:
137 / 137 families.

### Safety rules implemented

Original/source definitions are never changed:
- all T1/T2/T3 blocks remain byte-identical;
- all native Orange T4 blocks remain byte-identical;
- all native special launcher blueprint blocks remain byte-identical;
- all native Exotic T4 blocks remain byte-identical.

Custom sibling structure:
- CategoryType_Collectable
- ItemType(ItemType_CraftPlan)
- CraftplanType("Weapon")
- Color(Color_Exotic)
- ScaleWithPlayerRank(original family)
- no ItemLevel
- no NextLevelBlueprintName
- deterministic custom blueprint ID / UID
- native entitlement markers DLC(...) / LinkedDocket(...) are carried over when present rather than intentionally bypassed
- normal 106-family recipe uses native Exotic firearm/melee recipe pattern
- 10 edge sibling blueprints preserve source RequiredItem recipe identity

Delivery:
- use the exact existing Phase B weapon+blueprint ItemBundle.
- for the 116 custom families, append the matching custom Exotic sibling as another BundleItems entry.
- no change to bundle identity, lootset identity, route topology or route weights.
- 21 native Exotic families already carry the native T4 via the proven Phase B pair and are not touched.

Explicitly unchanged:
- default.loot
- tbp_lootpools_global_v1.loot
- tbp_lootsets_global_v1.loot
- LootedObject topology
- infected route weights
- resources
- charm
- Night Sovereign
- stash
- inventory versioning
- player_variables
- save format

Runtime overlay writer:
- ZIP_DEFLATED
- compresslevel 9
- deterministic ZipInfo timestamp
- external_attr 0x01800000
- create_system 3

### Static validation

SELFTEST PASS:
- 137/137 live-manifest family universe represented
- exact 2041 Phase B pair-bundle manifest retained
- 21 native Exotic families reused
- 116 custom standalone Exotic sibling definitions generated
- 1726 exact non-native-Exotic pair bundles enriched
- all original/source blueprint blocks byte-identical
- every 137 family bundle has an Exotic-blueprint candidate after patch
- custom siblings contain Color_Exotic + correct ScaleWithPlayerRank and no ItemLevel
- Phase B topology untouched
- package ZIP integrity PASS

### Runtime gate remains mandatory

After final clean reinstall / Steam verify:
1. confirm legitimate DLC detection is healthy before any mod;
2. install/restore proven Phase B Broad Final V2;
3. run All137 V2 self-test;
4. install one All137 V2 overlay;
5. verify several ordinary generated melee/firearm families;
6. verify at least one native Orange-T4 edge family uses the separate sibling without breaking its native T4;
7. verify Flamethrower, GrenadeLauncher and SawbladeLauncher sibling blueprint behavior;
8. verify crafted weapon is actually Exotic rather than merely showing an Exotic blueprint;
9. verify native Legend/workbench scaling remains normal;
10. save/reload and confirm rarity/stats/inventory/DLC state remain healthy.

Until that consolidated runtime gate passes:
EXOTIC ALL137 V2 = CANDIDATE / UNPROVEN.


## Exotic All137 V2 runtime result — HARD REJECTED

User installed/tested GH1_PHASE_C_EXOTIC_ALL137_OFFLINE_CANDIDATE_V2 on the current broken-DLC environment and reported that V2 also produced no useful Exotic result.

For project purposes this is a functional failure of the blueprint-side architecture:
- standalone custom Color_Exotic sibling blueprints are not sufficient;
- appending those siblings to the proven Phase B pair bundles is not sufficient;
- do not continue by cloning more T4 craftplans or changing T1/T2/T3;
- keep Phase B weapon+matching-blueprint architecture frozen.

Important interpretation:
Color(Color_Exotic) on a craftplan is now treated as blueprint/UI/acquisition metadata, not as sufficient proof that the crafted weapon instance itself will be Exotic.

This is consistent with the fact that native loot already has independent ColorSet_ExoticOnly routing and the game tracks Exotic weapon pickup separately from craftplan color.

### New Phase C direction

Stop blueprint-side Exotic mutation.

Next research target is weapon-instance / generation-side Exotic creation:
1. identify how ColorSet_ExoticOnly affects generated weapon instances;
2. compare native Exotic loot-generated weapons to the same/similar family generated at lower rarity;
3. locate rarity/affix roll inputs outside craftplan definitions;
4. determine whether a crafted weapon can be routed through the same native item-generation path or whether Exotic should remain a loot-only/native-drop property;
5. do not mass-edit weapon definitions until one-family weapon-side mechanism is statically isolated.

V2 and the earlier 127/137 candidate are now historical rejected experiments, not final-build components.


## Runtime clarification — workbench upgrade path itself stops at Legendary

User clarified the failure is not merely that the crafted weapon did not display Exotic color.

Observed runtime behavior:
- once a weapon blueprint reaches its current Legendary terminal tier, the workbench no longer presents any upgrade option;
- there is no visible Legendary -> Exotic / Iconic upgrade action;
- therefore blueprint-side Exotic experiments failed at the progression/UI gate before rarity output could even be meaningfully validated.

This changes the Phase C interpretation again.

### Correct current model

The normal blueprint upgrade graph is proven to be finite:
- ItemLevel + NextLevelBlueprintName drive visible T1/T2/T3 style progression;
- the user's runtime shows the ordinary Legendary terminal blueprint has no further upgrade option;
- standalone native Color_Exotic T4 blueprints exist, but their existence does NOT prove they are reached by upgrading a Legendary blueprint;
- rejected POC1 already showed that manually adding a T3 -> T4 next link was insufficient to make the workbench expose the desired Exotic upgrade.

Therefore:
- do NOT treat Exotic/Iconic as merely another color on the existing Legendary upgrade chain;
- do NOT keep cloning T4 blueprints as if the normal workbench graph will consume them;
- the next investigation target is the workbench/progression eligibility logic that decides whether a craftplan is upgradeable and what tiers are valid.

### Iconic note

No weapon-rarity symbol equivalent to Color_Iconic has been proven in the audited data so far. Do not invent an Iconic craftplan tier or color enum until exact current-version evidence is extracted.

### Next safe research target

Find current-version code/data governing:
- ItemLevel(min,max) interpretation;
- NextLevelBlueprintName resolution;
- workbench recipe/blueprint upgrade eligibility;
- any hardcoded maximum tier/rank table;
- any Exotic/Iconic-specific unlock or upgrade category;
- whether native Exotic T4 blueprints are direct-acquisition craftplans rather than successors.

Only after that gate is identified should another Exotic/upper-tier POC be designed.


## New runtime evidence — native Iconic Blueprint exists

User supplied a runtime screenshot of the workbench showing:

- weapon: Mechanical Reconstructor
- UI label: ICONIC BLUEPRINT
- visible blueprint level: 30
- 1920 total/base damage in the shown state
- 3 affixes
- 160 durability
- normal crafting-material requirements are displayed
- Craft is present but disabled in the screenshot because Inventory Full

This is direct runtime evidence that the game has a native Iconic blueprint state. It invalidates any model that assumes Legendary is the globally highest blueprint rarity/state.

Important limitation:
the screenshot proves existence/craftability of an Iconic blueprint, but does NOT by itself prove that a normal Legendary blueprint reaches Iconic through NextLevelBlueprintName or that Iconic corresponds to a guessed T5.

## External research signal — Upgrade and Enhance appear distinct

Public Nexus research identified:
- “Free Blueprints Craft and Upgrade (DLTB)” describes craft, upgrade, and enhance as distinct supported actions.
- Its changelog explicitly mentions fixing material cost for “enhance exotic weapons.”
- Another current mod (“Up to Date V2”) states that Iconic weapon blueprints are explicit unlockable blueprint items and notes that some Iconic blueprint unlock behavior changed in later game updates.

Treat this only as research direction, not as canonical game-data proof.

Current hypothesis to test:
- normal tier progression may end at Legendary;
- Exotic/Iconic may use a separate Enhance / upper-tier system rather than ordinary NextLevelBlueprintName chaining.

Do NOT assume T5=Exotic or T6=Iconic until current-version data proves it.

## Deep Blueprint Collector V2

Artifact:
GH1_PHASE_C_DEEP_BLUEPRINT_COLLECTOR_V2.zip

SHA256:
2b4cf17662af48eebc41d7894999e0c5352fa728893dbf2cb5b7aaa57f4e4786

Status:
READ-ONLY collector; synthetic self-test PASS.

Purpose:
- scan all installed dataN.pak with provenance;
- data0/data1 classified OFFICIAL, data2+ classified OVERLAY;
- parse every discovered weapon craftplan block;
- record Color, ItemLevel, NextLevelBlueprintName, ScaleWithPlayerRank, DLC, LinkedDocket, RequiredItem, AlternativePrice and raw block;
- map exact Craftplan references;
- search for Mechanical Reconstructor, Iconic, Exotic, Enhance, Upgrade and Blueprint;
- produce JSON, TXT and blueprint graph CSV;
- make no assumptions about T5/T6.

Immediate next action:
wait for the user’s Deep Blueprint Collector V2 output. Use the live current-version result to isolate the exact native Iconic/Enhance architecture before building another runtime POC.


## Deep Blueprint Collector V2 — decisive upper-tier findings

User ran GH1_PHASE_C_DEEP_BLUEPRINT_COLLECTOR_V2 against the current 1.71-era install.

Official data summary:
- official weapon blueprint blocks: 169
- official colors: Orange 56 / Blue 44 / Violet 48 / Exotic 21
- ItemLevel distribution includes exactly four ItemLevel(3,4) blueprints and four ItemLevel(4,4) blueprints
- 29 T4 blueprint blocks total
- GUI contains distinct blueprint-upgrade and weapon-enhance modes

Critical GUI fields found in official files:
- GuiInventoryItemData.m_HigherLevelBlueprint
- GuiInventoryItemData.m_CanAffordAlternatePrice
- GuiInventoryItemData.m_UpgradeItemLevel
- GuiInventoryItemData.m_MaxItemLevel
- GuiInventoryItemData.m_ItemLevel
- GuiItemTooltip.m_WeaponBlueprintUpgradeMode
- GuiItemTooltip.m_WeaponEnhanceMode
- GuiShopItemData.m_ShowUpgrade
- GuiShopItemData.m_ShowEnhance
- GuiShopItemData.m_CanEnhance

Official inv_item_slot_symbol logic shows blueprint-upgrade availability depends on a non-null m_HigherLevelBlueprint together with m_CanAffordAlternatePrice.

Official T3 -> T4 upgrade examples use:
T3:
- ItemLevel(3,4)
- NextLevelBlueprintName(T4)

T4:
- AlternativePrice(...)
- ItemLevel(4,4)

This explains an important defect in rejected POC1: its custom T4 had neither ItemLevel(4,4) nor AlternativePrice, so it did not satisfy the actual native upgrade data shape.

### Exact Mechanical Reconstructor mapping

Legend progression Reward level 40:
- weapon: dlc_ft_WPN_1HB_STK_X_r15
- blueprint: Craftplan_dlc_ft_WPN_1HB_STK_X_T4_Blueprint
- IncludesBlueprint()

Exact official blueprint:
- Color(Color_Exotic)
- ScaleWithPlayerRank("dlc_ft_WPN_1HB_STK_X_r")
- no ItemLevel
- no NextLevelBlueprintName

User screenshot shows this exact native reward family as:
MECHANICAL RECONSTRUCTOR — ICONIC BLUEPRINT.

Therefore for this native final blueprint, Color_Exotic maps to the user-visible Iconic blueprint presentation. It is acquired directly rather than through a lower-tier chain.

### New clean-room hypothesis

To make an ordinary generated T1/T2/T3 family actually upgrade to an Iconic final blueprint, combine two separately proven native structures:
1. upgrade gate structure from official T3->T4 chains:
   - all chain max tier raised to 4
   - T3 NextLevelBlueprintName(T4)
   - target T4 ItemLevel(4,4)
   - target T4 AlternativePrice(...)
2. Iconic presentation/final blueprint structure:
   - Color(Color_Exotic)
   - same ScaleWithPlayerRank family

This hybrid does not exist as an official block and therefore remains a hypothesis until runtime tested.

## GH1 Phase C Iconic Chain POC3 V1

Artifact:
GH1_PHASE_C_ICONIC_CHAIN_POC3_V1.zip

Package SHA256:
84b98107d505125155074a699b3d9162e6ef5fb9aa54674983825c7843948c87

Target:
dlc_ft_firearm_pistol_b_legendary_r

Mutation:
- T1 ItemLevel(1,3) -> ItemLevel(1,4)
- T2 ItemLevel(2,3) -> ItemLevel(2,4)
- T3 ItemLevel(3,3) -> ItemLevel(3,4)
- T3 NextLevelBlueprintName -> custom T4
- custom T4:
  - Color(Color_Exotic)
  - ScaleWithPlayerRank(same family)
  - AlternativePrice("Craft_Scrap",1)
  - ItemLevel(4,4)
  - no further Next

Packaging:
- one-family only
- dynamic effective collectables source
- ZIP_DEFLATED proven writer conventions
- no loot route/LootedObject/save/stash/player_variables/DLC mutation
- exact marker uninstall

Static selftest: PASS.

Runtime questions:
A. Does T3 now expose an upgrade button?
B. Does upgraded T4 show ICONIC BLUEPRINT?
C. Does crafting from T4 produce an Iconic weapon?

Do not mass-expand until A/B/C are tested.


## POC3 screenshot review — target mismatch, result INCONCLUSIVE

User supplied two runtime screenshots:
- .38 Revolver Legendary Blueprint: no right-side "NEXT BLUEPRINT UPGRADE" panel; only Craft / Pin Blueprint.
- Predator Epic Blueprint: normal right-side "NEXT BLUEPRINT UPGRADE" panel to Legendary is visible.

Important correction:
POC3 targeted:
- family: dlc_ft_firearm_pistol_b_legendary_r
- chain: Craftplan_GH1_dlc_ft_firearm_pistol_b_legendary_T1/T2/T3_Blueprint

The screenshot test target is .38 Revolver, whose generated Phase B family is:
- dlc_ft_firearm_revolver_c_legendary_r
- chain: Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T1/T2/T3_Blueprint

Therefore the screenshot does not validate the POC3 target. POC3 is not promoted and not treated as GREEN, but this specific test is INCONCLUSIVE rather than a clean architectural rejection.

Deep collector V2 also shows the generated .38 Revolver T2/T3 chain uses RequiredItemToShowInShop(previous blueprint) in addition to ItemLevel / NextLevelBlueprintName / AlternativePrice.

## Exact .38 Revolver Iconic POC4 V1

Artifact:
GH1_PHASE_C_38REVOLVER_ICONIC_POC4_V1.zip

Package SHA256:
0bae4f8699d63f10d9cd17ef914659cbc0882b9644e60326055024aa3094ee20

Status:
RUNTIME POC / UNPROVEN

Exact target:
- dlc_ft_firearm_revolver_c_legendary_r
- expected UI name: .38 Revolver

Patch:
- T1 ItemLevel(1,3) -> ItemLevel(1,4)
- T2 ItemLevel(2,3) -> ItemLevel(2,4)
- T3 ItemLevel(3,3) -> ItemLevel(3,4)
- T3 NextLevelBlueprintName -> new custom T4
- T4 cloned from exact generated Legendary T3 block, then:
  - Color(Color_Exotic)
  - ItemLevel(4,4)
  - RequiredItemToShowInShop(T3)
  - preserves T3 AlternativePrice fields
  - preserves exact ScaleWithPlayerRank family
  - new deterministic UID
  - no further NextLevelBlueprintName

Installer auto-removes only exact old experimental marker PAKs:
- POC1
- POC3
- Exotic All137 V2
It does not remove the proven Phase B stack.

Runtime gate:
1. install POC4;
2. confirm STATUS reports exact .38 Revolver chain T3 max 4 + T3->T4;
3. select .38 Revolver Legendary Blueprint in workbench;
4. check whether right-side NEXT BLUEPRINT UPGRADE panel appears;
5. if yes, upgrade and verify whether T4 UI says ICONIC BLUEPRINT;
6. craft and verify resulting weapon rarity.

Do not scale beyond one family until the right-side upgrade panel is runtime GREEN.
