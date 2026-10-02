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


## POC4 runtime result — HARD REJECTED

The exact .38 Revolver target was tested:
- family: dlc_ft_firearm_revolver_c_legendary_r
- runtime UI still showed only Legendary Blueprint
- no right-side NEXT BLUEPRINT UPGRADE panel
- therefore the collectables-only chain extension remained insufficient even on the exact target family.

POC4 is HARD REJECTED.

## New evidence from Deep Blueprint Collector V2 — Blueprints_Upgrades registry

Deep Collector V2 exposed the official workbench shop registry:

scripts/trading/shop_item_sets.scr

ItemSet("Blueprints_Upgrades")
{
    AllItemsAvailableInStore();
    ...
    Item("<weapon T2 blueprint>");
    Item("<weapon T3 blueprint>");
    Item("<weapon T4 blueprint>");
}

The official GUI also contains an internal comment:
"...but if it's in BlueprintUpgrades in FT, show it, since it's needed to progress there"

and uses EMenuShopMode value:
CraftMaster_BlueprintUpgrades.

Important consequence:
GH1 generated blueprint chains were created only in collectables_ft.scr and were not registered in the official Blueprints_Upgrades ItemSet because Phase B overlays do not carry scripts/trading/shop_item_sets.scr.

This is now a concrete missing integration layer that all prior Exotic/Iconic chain POCs lacked.

Official upper-tier data also confirms:
- only four official T3->T4 weapon chains exist in current audited data;
- those chains are Color_Violet T3 -> Color_Orange T4 (Epic -> Legendary);
- official Color_Exotic / runtime Iconic weapon blueprints are standalone and generally have no ItemLevel / NextLevelBlueprintName.

Therefore native Legendary -> Iconic via the normal upgrade panel remains unproven; however the missing Blueprints_Upgrades registration must be tested before declaring the engine incapable of extending the chain.

## POC5 — .38 Revolver + official Blueprints_Upgrades registry

Artifact:
GH1_PHASE_C_38REVOLVER_ICONIC_POC5_REGISTRY_V1.zip

SHA256:
4ff48bcd67a4b8e24ff9cf11c64e507fac3b60bcea2b060c350044775c143516

Target:
dlc_ft_firearm_revolver_c_legendary_r

POC5 patches both:
1. scripts/inventory/collectables_ft.scr
2. scripts/trading/shop_item_sets.scr

Collectables:
- T1 ItemLevel 1/3 -> 1/4
- T2 2/3 -> 2/4
- T3 3/3 -> 3/4
- T3 Next -> custom T4
- T4 Color_Exotic
- T4 ItemLevel(4,4)
- T4 RequiredItemToShowInShop(T3)
- T4 preserves generated-family pricing / ScaleWithPlayerRank structure

Workbench registry:
Blueprints_Upgrades receives:
- generated T2
- generated T3
- custom T4

Installer removes only exact rejected experiment marker PAKs before building; proven Phase B stack is preserved.

Static selftest:
PASS — collectables chain + official Blueprints_Upgrades registry both patched.

Runtime gate:
1. status must show registry T2/T3/T4 true;
2. exact .38 Revolver Legendary blueprint must be checked for NEXT BLUEPRINT UPGRADE panel;
3. if panel appears, upgrade and verify runtime Iconic label / crafted weapon result.


## Runtime result — POC5 registry upgrade attempt HARD REJECTED

User tested the exact .38 Revolver generated family after POC5 registered generated T2/T3/T4 in the official Blueprints_Upgrades ItemSet.

Observed:
- .38 Revolver still displayed only Craft / Pin Blueprint.
- no NEXT BLUEPRINT UPGRADE panel appeared.

Therefore the Legendary -> Iconic path through the normal blueprint-upgrade panel is now considered HARD REJECTED for this project.

Do not spend more POCs trying to force Iconic as the next normal blueprint tier through:
- ItemLevel max extension,
- NextLevelBlueprintName,
- RequiredItemToShowInShop,
- AlternativePrice,
- or Blueprints_Upgrades registry membership.

Current-version native evidence remains:
- native Color_Exotic/Iconic weapon blueprints are generally standalone;
- they commonly omit ItemLevel;
- they commonly omit NextLevelBlueprintName;
- official T3 -> T4 upgrade chains observed in current data are ordinary Epic/Violet -> Legendary/Orange progression, not Legendary -> Iconic.

## POC6 — standalone Iconic acquisition via vendor unlock

Artifact:
GH1_PHASE_C_38REVOLVER_STANDALONE_ICONIC_POC6_V1.zip

Package SHA256:
e97381f12a562c21391cabcc226ad5811130a872a48f1ca1c8c92ff6564e5fb5

Target family:
dlc_ft_firearm_revolver_c_legendary_r

Custom blueprint:
Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_Iconic_Blueprint

Architecture:
- T1/T2/T3 are untouched;
- define one standalone weapon craftplan;
- Color(Color_Exotic);
- ScaleWithPlayerRank(target family);
- no ItemLevel;
- no NextLevelBlueprintName;
- native-style firearm recipe 35 Scrap / 12 Wiring / 12 Leather / 6 Firearm Scrap;
- expose the new blueprint in both Hub1_Unlocks and Hub2_Unlocks in current effective shop_item_sets.scr;
- acquisition therefore follows the same vendor-exposure layer used by the previously audited Nexus 686 blueprint mod, without copying its stale full files.

Runtime test gate:
1. confirm blueprint appears at a HUB 1 or HUB 2 trader;
2. buy/acquire it;
3. confirm workbench title is ICONIC BLUEPRINT;
4. craft it;
5. confirm resulting weapon instance is actually Iconic.

If this succeeds, scale standalone Iconic acquisition rather than reopening the rejected normal-upgrade-panel architecture.


## POC5 runtime result — HARD REJECTED

The exact .38 Revolver Legendary blueprint was tested after registering its generated T2/T3/T4 entries in the official Blueprints_Upgrades ItemSet.

Runtime result:
- the workbench still showed only Craft / Pin Blueprint;
- the right-side NEXT BLUEPRINT UPGRADE panel did not appear.

Therefore:
- collectables chain + Blueprints_Upgrades registry registration is still insufficient to make this existing Legendary blueprint expose an Iconic successor;
- do not continue the Legendary -> Iconic upgrade-panel architecture.

## POC7 — convert the already-owned terminal blueprint in place

User requested avoiding any reacquisition because already-owned blueprints may not be obtainable again through the same acquisition route.

POC7 therefore reuses the exact existing owned blueprint ID:
Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T3_Blueprint

No new blueprint ID is created.

POC7 changes only that existing terminal definition:
- Color(Color_Orange) -> Color(Color_Exotic)
- remove ItemLevel(...)
- remove NextLevelBlueprintName(...)
- remove RequiredItemToShowInShop(...)
- remove AlternativePrice(...)

Identity and ownership-facing fields remain identical:
- exact item ID
- Name
- Description
- ScaleWithPlayerRank
- HudIcon
- UID
- crafting recipe
- crafting sounds

Rationale:
current native Color_Exotic blueprints displayed by the game as ICONIC BLUEPRINT are standalone and do not carry ItemLevel or NextLevelBlueprintName.

Artifact:
GH1_PHASE_C_38REVOLVER_EXISTING_BP_ICONIC_POC7_V1.zip

SHA256:
3b7c2e97bb8617135bf654a571305498af7a4741f6281522407910876f846115

Status:
CANDIDATE / runtime test pending.

Runtime gate:
1. install POC7;
2. status must show same T3 blueprint ID, Color_Exotic, and no ItemLevel/Next/shop-gate/AlternativePrice;
3. open the already-owned .38 Revolver blueprint in the workbench;
4. check whether its title now reads ICONIC BLUEPRINT;
5. check craft availability;
6. craft and inspect whether the resulting weapon instance is Iconic.

This test specifically avoids any vendor/drop reacquisition requirement.


## Runtime breakthrough — POC6 standalone Iconic path functionally GREEN

User runtime-tested:
GH1_PHASE_C_38REVOLVER_STANDALONE_ICONIC_POC6_V1.zip

Observed:
- after installing POC6 and opening trader, the exposed blueprint appeared as Sunray Iconic rather than .38 Revolver;
- after purchase, the blueprint could be crafted;
- crafted weapon was genuinely Iconic;
- crafted weapon level followed current player level.

Therefore the following mechanism is runtime GREEN:
- standalone weapon craftplan;
- Color(Color_Exotic);
- ScaleWithPlayerRank(<weapon family>);
- no ItemLevel;
- no NextLevelBlueprintName;
- direct acquisition/exposure;
- crafted result can be genuinely Iconic and player-level-scaled.

Important identity correction:
POC6 targeted family:
dlc_ft_firearm_revolver_c_legendary_r

Runtime UI showed Sunray.
Therefore previous assumption that this family corresponds to .38 Revolver is wrong or at least unproven.

Consequences:
- POC4/POC5 tests aimed at .38 Revolver using this family do not prove anything about the actual .38 family.
- POC7 uses the SAME family/blueprint identity and should be interpreted as an existing-owned Sunray blueprint conversion test unless runtime proves otherwise.
- before mass rollout, build a reliable family->localized weapon-name mapper from current game data.

Status:
STANDALONE ICONIC ARCHITECTURE = FUNCTIONALLY GREEN on current broken-DLC environment.
Clean reinstall/save-persistence/DLC health still pending final validation.


## POC7 runtime result — existing T3 conversion breaks upgrade transaction

User tested the existing-blueprint conversion POC7 on the family previously assumed to be .38 Revolver.

Runtime identity correction:
- the family `dlc_ft_firearm_revolver_c_legendary_r` is observed in UI as Sunray, not .38 Revolver.

Runtime behavior with POC7:
- after upgrading Sunray from lower tier to Epic, the next upgrade preview skipped Legendary and displayed the converted T3 as Iconic;
- holding the upgrade input did not complete the transaction;
- blueprint remained at the prior tier;
- the Iconic upgrade preview remained visible and could be spammed without progress.

Interpretation:
POC7 changed the same T3 item ID to standalone Iconic style by removing:
- ItemLevel
- AlternativePrice
- RequiredItemToShowInShop
- progression metadata

T2 still pointed at that same T3 ID, so UI resolved the target rarity as Iconic, but the target no longer had valid upgrade-transaction metadata. This explains the stuck upgrade behavior.

POC7 = HARD REJECTED.

## POC8 — existing Sunray T3, color-only mutation

Artifact:
GH1_PHASE_C_SUNRAY_EXISTING_T3_ICONIC_POC8_V1.zip

SHA256:
4872330491c4963aadc457625225f9f77e76324048579b0c4a2f8306cb13ccfe

Target:
`Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T3_Blueprint`

Observed UI identity:
Sunray

POC8 changes exactly one semantic field:
- `Color(Color_Orange)` -> `Color(Color_Exotic)`

Everything else in T3 is preserved byte-for-byte:
- same blueprint ID
- same UID
- same Name/Description
- same ScaleWithPlayerRank
- same ItemLevel(3,3)
- same AlternativePrice entries
- same RequiredItemToShowInShop
- same crafting recipe
- same crafting sounds

Purpose:
test whether the existing upgrade-valid T3 can remain a valid T2->T3 transaction while presenting/crafting as Iconic purely through Color_Exotic.

Static selftest PASS.


## POC8 runtime result — GREEN

User runtime-tested the existing generated Sunray T3 blueprint with ONLY:
Color(Color_Orange) -> Color(Color_Exotic)

All upgrade metadata remained intact.

Observed runtime:
- Epic upgraded directly to Iconic successfully;
- resulting blueprint state was genuinely Iconic;
- crafted weapon was genuinely Iconic.

This proves the minimal generated-blueprint architecture:
- keep the SAME T3 blueprint ID;
- keep ItemLevel(3,3);
- keep AlternativePrice;
- keep RequiredItemToShowInShop;
- keep recipe / UID / ScaleWithPlayerRank / ownership identity;
- change ONLY Color_Orange -> Color_Exotic.

Generated progression therefore becomes:
Blue/Rare -> Violet/Epic -> Exotic/Iconic
rather than creating a separate Legendary -> Iconic step.

This is now the preferred Phase C architecture for generated non-native weapon families.

## ALL88 mass Iconic final-test candidate V1

Artifact:
GH1_PHASE_C_ALL88_EXISTING_T3_ICONIC_FINALTEST_V1.zip

SHA256:
ed756aeb7b3a530ef356315d87c989168afc30019c8cc817d849db791555cf61

Scope locked from actual Phase B final coverage + Exotic scanner:
- 88 generated non-native families
- 73 melee
- 15 firearm
- 49 native families explicitly excluded

Static source facts:
- all 88 generated families have T1/T2/T3;
- all 88 generated T3 blocks were Color_Orange at scan time;
- all 88 generated T3 blocks use ItemLevel(3,3).

Mass mutation:
- exactly 88 generated T3 blocks;
- Color(Color_Orange) -> Color(Color_Exotic) ONLY.

Invariant validation:
- T1/T2 untouched;
- T3 ItemLevel(3,3) preserved;
- T3 AlternativePrice preserved;
- T3 RequiredItemToShowInShop preserved;
- blueprint ID / UID / recipe / Name / Description / ScaleWithPlayerRank preserved;
- native families untouched;
- Phase B loot / bundle / route topology untouched.

Selftest:
PASS — 88/88 targets patched, only Color changed, upgrade metadata preserved.

Runtime gate requested:
- test multiple melee families;
- test multiple firearm families;
- verify Epic -> Iconic upgrade completes;
- verify blueprint displays ICONIC BLUEPRINT;
- verify crafted weapon is genuinely Iconic;
- verify ScaleWithPlayerRank output follows player level;
- verify native blueprint families remain unchanged.

Status:
CANDIDATE pending broad runtime test.


## ALL88 mass Iconic final-test V1 installer result — STATIC MATCHER REJECTED

User ran GH1_PHASE_C_ALL88_EXISTING_T3_ICONIC_FINALTEST_V1.zip.

Observed installer behavior:
- installer correctly auto-removed the old POC8 marker PAK;
- install then stopped before writing the new overlay;
- error reported many generated melee T3 families as missing;
- no ALL88 V1 mass overlay was installed.

The missing list pattern started with the WPN melee families while the firearm-generated targets were largely resolved. This exposed a matcher defect in V1 rather than a runtime Iconic failure.

Root cause:
V1 used ScaleWithPlayerRank family strings as the primary identity key. Current generated melee data contains mixed capitalization conventions across blueprint/family identifiers (for example WPN / 15HB / 1HB variants). Exact family-string matching was therefore too brittle.

Safety outcome:
GOOD FAIL-SAFE. V1 aborted before generating/writing a partial PAK.

Do not reuse the V1 family-primary matcher.

## ALL88 mass Iconic final-test V2

Artifact:
GH1_PHASE_C_ALL88_EXISTING_T3_ICONIC_FINALTEST_V2.zip

SHA256:
f757899cc49a81474615c0bc3b8c12499f85e70da945b74ce2099357424a9818

Scope:
- 88 generated non-native families
- 73 melee
- 15 firearm
- 49 native families excluded

Critical V2 correction:
- primary target identity is now the EXACT T3 blueprint ID captured by the live Exotic Workbench Scanner;
- blueprint IDs are matched case-insensitively;
- ScaleWithPlayerRank is only a secondary sanity check and is also compared case-insensitively.

Mutation remains identical to runtime-GREEN POC8:
Color(Color_Orange) -> Color(Color_Exotic) ONLY.

All other T3 data must remain unchanged:
- blueprint ID
- UID
- ItemLevel(3,3)
- AlternativePrice
- RequiredItemToShowInShop
- recipe
- Name / Description
- ScaleWithPlayerRank
- T1/T2
- Phase B loot/bundle/routes

V2 synthetic validation:
SELFTEST PASS
- 88 exact T3 blueprint IDs resolved;
- family casing differences deliberately injected and tolerated;
- 88/88 targets changed to Color_Exotic;
- no mutation outside Color();
- ZIP integrity PASS.

Runtime expected status after install:
- EXACT TARGET IDS FOUND: 88 / 88
- ICONIC/Color_Exotic: 88
- LEGENDARY/Color_Orange: 0
- OTHER: 0

Status:
RUNTIME FINAL-TEST CANDIDATE.


## Remaining migration edge case after All88/P8 architecture

User reported one final issue before considering Phase C maximally proven:
- generated blueprints that were already owned/saved in terminal Legendary state before the Iconic conversion do not automatically gain an Iconic upgrade path.

Interpretation:
- POC8/All88 color-only conversion is runtime GREEN for blueprints still progressing through T1/T2, because the transition into T3 resolves the current T3 definition as Color_Exotic/Iconic.
- pre-existing terminal T3 ownership appears to retain legacy terminal state and requires an explicit migration path.

### POC9 — correct Sunray legacy T3 -> Iconic T4 migration

Artifact:
GH1_PHASE_C_SUNRAY_LEGACY_T3_TO_ICONIC_POC9_V1.zip

SHA256:
4cdd1869e28fb9ca31d750a2ef1491b000248378ce58d446ac1513f80e6256d3

Correct runtime-mapped family:
dlc_ft_firearm_revolver_c_legendary_r = Sunray in the user's UI.

POC9 deliberately removes All88/P8 experimental overlays before constructing a true four-step chain from the baseline generated chain:
- T1 Blue: ItemLevel(1,4)
- T2 Epic/Violet: ItemLevel(2,4)
- T3 Legendary/Orange: ItemLevel(3,4), NextLevelBlueprintName(T4)
- T4 Iconic/Color_Exotic: ItemLevel(4,4), RequiredItemToShowInShop(T3)

T2/T3/T4 are also registered in the official Blueprints_Upgrades ItemSet.

Purpose:
test whether an already-owned/saved Sunray T3 Legendary blueprint can now expose NEXT BLUEPRINT UPGRADE and complete a migration to T4 Iconic.

If runtime GREEN:
- keep color-only All88 behavior for ordinary T1/T2 progression OR replace with unified four-tier graph if desired;
- add a migration T4 layer for the 88 generated families so legacy T3 saves can reach Iconic;
- then re-run broad melee/firearm validation.

Status:
POC9 CANDIDATE / UNPROVEN pending runtime test.


## Legacy T3 migration result — POC9 HARD REJECTED

User runtime-tested the correct Sunray family with a true T3 Legendary -> T4 Iconic successor graph plus Blueprints_Upgrades registration.

Observed:
- already-owned/saved Legendary Sunray T3 still did NOT show NEXT BLUEPRINT UPGRADE.

Conclusion:
- for blueprints already persisted in the save as terminal T3/Legendary, changing the data definition to add a successor does not migrate the saved terminal state;
- Blueprints_Upgrades registration does not override that persisted terminal state;
- in-place legacy T3 -> T4 migration through the normal upgrade panel is HARD REJECTED.

Do not spend more time trying to retrofit a successor onto already-owned terminal T3 blueprints.

## Legacy migration fallback — POC10

Artifact:
GH1_PHASE_C_SUNRAY_LEGACY_MIGRATION_POC10_V1.zip

SHA256:
728326d79ff948583cf2e80b112451b8c26ff0ffb199f3acb55f557e1b333765

Architecture:
- preserve the user's old T3 Legendary blueprint;
- create one separate standalone Color_Exotic/Iconic migration blueprint;
- gate its vendor visibility with RequiredItemToShowInShop(old T3 ID);
- expose it through Hub1_Unlocks and Hub2_Unlocks;
- no save editing;
- no need to reacquire the old blueprint;
- POC6 already proved standalone Color_Exotic -> real Iconic craft + player-level scaling.

POC10 runtime gate:
- existing owner of legacy Sunray T3 should see the migration Iconic blueprint at Hub trader;
- after purchase it should display as ICONIC BLUEPRINT;
- crafted result should be Iconic and scale with player level.

If POC10 is GREEN, final Phase C should use a hybrid:
1. POC8-style Color_Orange -> Color_Exotic on generated T3 for blueprints that are still progressing through T1/T2;
2. companion migration Iconic siblings for users who already have terminal T3 persisted in the save.


## Deep blocker scan V3 — requested after legacy-T3 migration failure

User hypothesis to investigate:
the workbench may visually expose upgrade progression through one gate while a separate gate hard-limits an already-owned Legendary blueprint from progressing to Iconic.

This is explicitly treated as a hypothesis, not a conclusion.

New read-only collector:
GH1_PHASE_C_LEGEND_TO_ICONIC_BLOCKER_COLLECTOR_V3.zip

Package SHA256:
b4332353d1405ad9b98360d7f639f2b54a6aa05587c705cbf544c68eed4214cf

Purpose:
find every reachable data/runtime clue related to Legendary -> Iconic blueprint progression, especially blockers outside collectables_ft.scr and Blueprints_Upgrades.

Collector targets:
- BlueprintUpgrades / Blueprints_Upgrades
- NextLevelBlueprintName
- HigherLevelBlueprint / m_HigherLevelBlueprint
- ItemLevel / m_ItemLevel
- MaxItemLevel / m_MaxItemLevel
- UpgradeItemLevel / m_UpgradeItemLevel
- CanUpgrade / IsUpgradeable / MaxLevel / IsMaxLevel / terminal-state symbols
- CanAfford / m_CanAffordAlternatePrice
- RequiredItemToShowInShop / AlternativePrice
- CraftMaster / unlock/progression symbols
- Color_Exotic / Iconic / Legendary / ColorSet
- Enhance / WeaponEnhancement subsystem symbols

Read-only coverage:
- relevant entries from every dataN.pak
- exact effective Sunray T1/T2/T3 definitions
- exact Blueprints_Upgrades / Hub1_Unlocks / Hub2_Unlocks item sets
- current upper-tier craftplans
- game x64 EXE/DLL ASCII + UTF-16 strings, scanned streaming
- Steam AppID 3008130 save files, scanned streaming for blueprint/tier strings only

Anti-hang design:
- no whole-PAK extraction
- max 32 MB per PAK entry
- EXE/DLL/save streaming in 4 MB chunks
- max 120 hits per file
- max 10,000 hits globally
- bounded context
- live progress output
- subprocess timeouts
- at most 100 latest save files
- one corrupt/slow entry is logged and skipped instead of stopping the scan

Expected user output:
GH1_PHASE_C_ICONIC_BLOCKER_SCAN_V3_<timestamp>.zip

Do not design another Legendary -> Iconic upgrade POC until this V3 result is analyzed.


## Legendary -> Iconic blocker collector V3 result + targeted V4 follow-up

User returned:
GH1_PHASE_C_ICONIC_BLOCKER_SCAN_V3_20261002_165501.zip

V3 key result:
- effective collectables owner at scan time was data6.pak from POC9;
- Sunray generated T1 was ItemLevel(1,4) and pointed to T2;
- T2 was ItemLevel(2,4) and pointed to T3;
- T3 was still Color_Orange, ItemLevel(3,4), and had NextLevelBlueprintName to the custom T4 Iconic migration blueprint;
- effective Blueprints_Upgrades registry contained the generated Sunray T2, T3 and custom T4;
- runtime nevertheless showed no NEXT BLUEPRINT UPGRADE for an already-owned terminal Legendary Sunray.

Therefore:
the POC9 failure is not explained by a missing collectables link or missing Blueprints_Upgrades registration. A runtime resolver / saved item state / other validation gate remains the primary suspect.

V3 also found GUI-facing symbols including:
m_HigherLevelBlueprint, m_ItemLevel, m_MaxItemLevel, m_UpgradeItemLevel,
m_CanAffordAlternatePrice, BlueprintUpgrades, UpgradeBlueprint, CanEnhance and WeaponEnhancement.

Important V3 limitation:
- generic PAK scanning reached the 10,000 hit global cap;
- only a small number of early binary hits were collected and no save hits made it into the result;
- the main DyingLightGame/gamedll/save-state hypothesis was therefore NOT adequately tested by V3.

Targeted V4 collector created:
GH1_PHASE_C_ICONIC_BLOCKER_TARGETED_COLLECTOR_V4.zip
SHA256:
d9fcd9ef8c30335c749499dc11f163d1b5cd7fce312dbdc426f8557ce0b6f137

V4 design:
1. scan save files FIRST, read-only and streaming;
2. scan only high-value game binaries SECOND:
   DyingLightGame_TheBeast_x64_rwdi.exe, gamedll_ph_x64_rwdi.dll,
   engine_x64_rwdi.dll, engine_core_x64_rwdi.dll, engine_foundation_x64_rwdi.dll,
   workshop_x64_rwdi.dll and RmluiAdapter_x64_rwdi.dll;
3. scan only selected workbench/inventory/trading PAK paths THIRD;
4. no global noisy PAK hit cap that can starve save/binary analysis;
5. keyword-centered context for one-line GUI JSON;
6. bounded 2 MB streaming chunks and 20 hits per keyword per file.

Do not design another Legendary->Iconic upgrade POC until V4 evidence is reviewed.


## Targeted blocker scan V4 — runtime gate evidence

User ran:
GH1_PHASE_C_ICONIC_BLOCKER_TARGETED_V4_20261002_170243.zip

V4 completed cleanly:
- 3 save/profile files scanned first;
- 7 target game binaries scanned;
- 15 high-value PAK paths targeted;
- 953 total hits;
- zero collector errors.

### POC9 data state is confirmed correct

Effective source was data6.pak.

Sunray generated chain in effective collectables:
- T1: Color_Blue, ItemLevel(1,4), Next -> T2
- T2: Color_Violet, ItemLevel(2,4), Next -> T3
- T3: Color_Orange, ItemLevel(3,4), Next -> custom T4 Iconic migration blueprint
- T4: Color_Exotic, ItemLevel(4,4), RequiredItemToShowInShop(T3)

Effective Blueprints_Upgrades ItemSet also contains:
- generated T2
- generated T3
- custom T4

Therefore POC9 runtime failure is NOT caused by the expected collectables chain or missing Blueprints_Upgrades registration.

### New runtime gate symbols found in gamedll

The current gamedll contains blueprint/runtime data fields:
- m_UpgradeItemLevel
- m_HigherLevelBlueprint
- m_CanAffordCraft
- m_ShowupgradeInfo
- m_IsBlueprint
- m_IsBlueprintAvailable
- m_HasABlueprintUpgrade
- m_MaxItemLevel
- m_ItemLevel
- m_CanAffordAlternatePrice

Tooltip/controller fields also include:
- m_DisableUpgrade
- m_WeaponBlueprintUpgradeMode
- m_WeaponEnhanceMode

Controller/action strings include:
- UpgradeWeaponBlueprint
- MenuShopController::UpgradeCurrentBlueprint
- FirstWorkbenchBlueprintUpgrade

GUI evidence:
shop_item_tooltip_addon_pc.gui controls blueprint-upgrade panel visibility from GuiShopItemData.m_ShowUpgrade.
The upgrade button disabled-state separately tracks m_CanAffordAlternatePrice.
Therefore visible upgrade UI is downstream of a runtime-computed resolver/state gate; editing ItemLevel/NextLevel/registry is not sufficient by itself.

### Save scan limitation / clue

V4 scanned the current settings/save/backup files before other phases and found zero plaintext occurrences of:
- generated Sunray T1/T2/T3/T4 IDs,
- family ID,
- ItemLevel,
- BlueprintUpgrade.

Do NOT interpret this as proof that save does not cache blueprint tier state. The save format is binary/serialized/compressed enough that plain string search cannot expose that state.

Current leading hypothesis, still unproven:
an already-owned terminal T3 may retain a serialized/runtime max-item-level / terminal state from the moment it was acquired, causing m_HasABlueprintUpgrade / m_ShowUpgrade / m_HigherLevelBlueprint to remain false/null even after later definition changes.

This hypothesis fits the observed split:
- POC8: T1/T2 progression creating/upgrading into the modified T3 successfully yields real Iconic.
- legacy T3 already owned before the patch does not gain a successor under POC9.

### External modding evidence

Current Nexus material also treats Legendary as the end of normal blueprint-upgrade progression in at least some store/blueprint implementations, while Iconic blueprints are commonly exposed/acquired separately. This supports, but does not prove, a separate upper-tier path.

### V5 next collector

Built:
GH1_PHASE_C_ICONIC_RUNTIME_GATE_COLLECTOR_V5.zip
SHA256:
d82b1e3392c03cd3bddf420feb820b7dac176ebfad93c91bd855c8626e15b643

V5 is narrower than V4 and scans:
- save codec/header/compression signatures first;
- only four main binaries;
- only five GUI files;
- newly discovered gate fields including m_ShowUpgrade, m_HasABlueprintUpgrade, m_DisableUpgrade, m_WeaponBlueprintUpgradeMode, and UpgradeCurrentBlueprint.

Safety:
read-only; no save/game modification; no full PAK crawl; bounded decompression and hit counts.


## Runtime gate collector V5 result — m_HigherLevelBlueprint is the decisive visible-upgrade gate

User returned:
GH1_PHASE_C_ICONIC_RUNTIME_GATE_V5_20261002_171316.zip

V5 completed without collector errors and produced 151 targeted hits.

### Save format
The current Steam save/profile files are GZIP containers:
- dltb_settings.dat: GZIP
- save_ft_0.sav: GZIP
- save_ft_0_chp000.sbk: GZIP

The main save and checkpoint decompress successfully.
After decompression there are still no plaintext hits for the exact generated Sunray T1/T2/T3/T4 IDs or family ID.
Therefore legacy blueprint state is serialized/binary after decompression; lack of plaintext IDs does NOT disprove persisted state.

The decompressed save does contain generic tutorial/progression strings such as FirstWorkbenchBlueprintUpgrade, confirming the decompressed payload is meaningful game state.

### Runtime data structures discovered
gamedll_ph_x64_rwdi.dll exposes GuiInventoryItemData blueprint fields:
- m_UpgradeItemLevel
- m_HigherLevelBlueprint
- m_CanAffordCraft
- m_ShowupgradeInfo
- m_IsBlueprint
- m_IsBlueprintAvailable
- m_HasABlueprintUpgrade

GuiShopItemData includes:
- m_CanUpgrade
- m_ShowUpgrade
- m_IsBlueprintUpgrade
- m_LowerLevelBlueprint

GuiItemTooltip includes:
- m_DisableUpgrade
- m_WeaponBlueprintUpgradeMode
- m_WeaponEnhanceMode

Controller actions include:
- UpgradeWeaponBlueprint
- MenuShopController::UpgradeCurrentBlueprint
- EnhanceWeapon
- CraftMaster_BlueprintUpgrades

### Exact GUI gate
gui/common_pc/inv_item_slot_symbol_pc.gui reads:
- GuiInventoryItemData.m_HigherLevelBlueprint
- GuiInventoryItemData.m_CanAffordAlternatePrice

It performs an IsNotNull test on m_HigherLevelBlueprint and ANDs that with m_CanAffordAlternatePrice before setting blueprint_upgrade_available visible.

Therefore the missing upgrade indicator for an already-owned legacy Legendary T3 is explained directly by the runtime resolver returning no higher-level blueprint pointer.
POC9 proved that merely editing ItemLevel/NextLevelBlueprintName/Blueprints_Upgrades does not cause that persisted item instance to receive a non-null m_HigherLevelBlueprint.

Current interpretation:
- data chain is correct;
- UI is not the primary blocker;
- the unresolved blocker is the runtime population of m_HigherLevelBlueprint / m_HasABlueprintUpgrade for the already-owned T3 instance.
- persisted/cached terminal blueprint state remains the strongest hypothesis, but binary serialization prevents declaring the exact saved field proven.

Do NOT patch GUI visibility alone: forcing the panel visible would not create a valid m_HigherLevelBlueprint object and could leave UpgradeCurrentBlueprint with no valid target.

## POC11 — no-trader Workbench migration path

V5 also confirmed a separate native workbench mode:
CraftMaster_BlueprintUpgrades

The menu GUI contains the explicit FT comment:
"...but if it's in BlueprintUpgrades in FT, show it, since it's needed to progress there"

Therefore a safer no-trader bypass is now being tested:
- do not modify legacy T1/T2/T3;
- create a standalone Color_Exotic Sunray migration blueprint;
- gate it with RequiredItemToShowInShop(legacy T3);
- register it ONLY in ItemSet("Blueprints_Upgrades");
- do NOT add it to Hub1_Unlocks / Hub2_Unlocks;
- rely on the Workbench Blueprint Upgrades mode to surface it as a separate progression entry rather than requiring the legacy T3's null m_HigherLevelBlueprint pointer.

Artifact:
GH1_PHASE_C_SUNRAY_WORKBENCH_MIGRATION_POC11_V1.zip

SHA256:
6da8bf28724cad236b7968e8d0cce656c41441040917140c95b423ba6644d606

Selftest:
PASS
- standalone Iconic migration definition;
- ownership gate = legacy Sunray T3;
- present in Blueprints_Upgrades;
- absent from Hub1_Unlocks and Hub2_Unlocks;
- T1/T2/T3 untouched.

Runtime test:
A) Iconic Sunray migration entry appears in Workbench -> Blueprint Upgrades?
B) Workbench can acquire/upgrade it?
C) it becomes ICONIC BLUEPRINT?
D) crafted weapon is true Iconic and player-level-scaled?

If POC11 is GREEN, prefer it over trader migration for already-owned legacy T3 blueprints.


## POC11 result + V6 runtime-xref direction

POC11 (Sunray standalone Iconic sibling exposed ONLY through ItemSet("Blueprints_Upgrades"), gated by legacy T3 ownership) was runtime tested.

Observed:
- Workbench still showed only the existing Sunray LEGENDARY BLUEPRINT.
- The standalone Iconic migration sibling did NOT appear as a separate workbench entry.

Conclusion:
- POC11 HARD REJECTED.
- Blueprints_Upgrades is not a free workbench catalog that independently exposes arbitrary craftplans.
- It participates only after the internal blueprint resolver/progression state considers an entry valid.

Evidence accumulated from V5:
- POC9 data graph was present correctly in effective data: T3 ItemLevel(3,4), T3 -> T4, T4 Color_Exotic/ItemLevel(4,4), registry entries present.
- Runtime still did not show NEXT BLUEPRINT UPGRADE.
- GUI/runtime fields of interest include m_HigherLevelBlueprint, m_HasABlueprintUpgrade, m_DisableUpgrade, m_WeaponBlueprintUpgradeMode, m_ShowUpgrade, m_MaxItemLevel, m_UpgradeItemLevel, m_CanAffordAlternatePrice.
- Workbench UI is downstream of runtime-resolved state; forcing presentation without a valid higher blueprint risks the POC7 failure mode (visible target but no transaction).

Next research tool:
GH1_PHASE_C_RUNTIME_XREF_COLLECTOR_V6.zip
Purpose:
- targeted PE64 xref/function extraction from gamedll_ph_x64_rwdi.dll and DyingLightGame_TheBeast_x64_rwdi.exe;
- locate exact runtime gate strings and reflection metadata;
- follow direct/indirect metadata pointers;
- scan executable sections for RIP-relative / immediate xrefs;
- use .pdata to recover function boundaries;
- extract only small relevant function snippets and descriptor neighborhoods for offline disassembly;
- no PAK/save scan and no modification.

Do not scale POC11.
Do not build another GUI-only bypass before runtime resolver logic is understood.


## V6 runtime xref analysis — field offsets recovered; string xrefs are reflection registration

User ran:
GH1_PHASE_C_RUNTIME_XREF_COLLECTOR_V6

gamedll_ph_x64_rwdi.dll SHA256:
ddb68c8f87ba2afd0e561b2d1adb9235467c29069fb1cd1619db81e1056378eb

V6 extracted 17 relevant gamedll functions and showed that direct xrefs to names such as
m_HigherLevelBlueprint / m_HasABlueprintUpgrade / m_DisableUpgrade are primarily generated
reflection-registration code, not the resolver logic itself.

However, the generated registration calls reveal exact field offsets:

GuiInventoryItemData:
- +0x130 m_MaxItemLevel
- +0x193 m_CanAffordAlternatePrice
- +0x3F0 m_UpgradeItemLevel
- +0x400 m_HigherLevelBlueprint
- +0x418 m_CanAffordCraft
- +0x419 m_ShowupgradeInfo
- +0x41A m_IsBlueprint
- +0x41B m_IsBlueprintAvailable
- +0x420 m_HasABlueprintUpgrade

Additional nearby exact reflection fields:
- +0x41D m_IsBlueprintPinned
- +0x41E m_CanPinBlueprint
- +0x41F m_CanUnPinBlueprint
- +0x421 m_IMDataWeaponCraftingCantCraft
- +0x422 m_IMDataWeaponEnhantingCantEnhant

GuiShopItemData:
- +0x5F1 m_CanCraft
- +0x5F2 m_CanEnhance
- +0x5F3 m_ShowEnhance
- +0x5F4 m_CanUpgrade
- +0x5F5 m_ShowCraft
- +0x5F6 m_ShowUpgrade
- +0x5F7 m_IsBlueprintUpgrade
- +0x600 m_LowerLevelBlueprint

GuiItemTooltip:
- +0x150 m_DisableUpgrade
- +0x151 m_WeaponBlueprintUpgradeMode

V6 also captured a real code candidate at RVA 0x00E5BC5D containing
MenuShopController::UpgradeCurrentBlueprint.

Interpretation:
The next useful reverse-engineering step is no longer string searching.
Search executable code for reads/writes to the exact field offsets above, recover the surrounding
functions using .pdata, and inspect those functions and their one-hop callees.

### V7 collector

Built:
GH1_PHASE_C_RUNTIME_FIELD_ACCESS_COLLECTOR_V7.zip

Purpose:
- one DLL only: gamedll_ph_x64_rwdi.dll;
- scan x64 [base + disp32] operands for exact recovered field offsets;
- classify likely read/write accesses;
- rank functions touching multiple upgrade-related fields;
- extract top functions with .pdata boundaries;
- extract one-hop callees;
- when DLL hash matches V6, seed known UpgradeCurrentBlueprint RVA 0x00E5BC5D and capture callers/callees;
- no PAK/save scan; read-only; bounded output.

Do not build another Iconic runtime POC until V7 identifies the actual resolver/field-population logic.


## V7 runtime field-access result — offset-only scan has false positives; class anchors recovered

User returned:
GH1_PHASE_C_RUNTIME_FIELD_ACCESS_V7_20261002_181616.zip

Current gamedll SHA256 still matches:
ddb68c8f87ba2afd0e561b2d1adb9235467c29069fb1cd1619db81e1056378eb

V7 produced:
- 11,005 raw field-offset access candidates
- 5,591 candidate functions
- 100 ranked primary functions
- 263 function snippets

Important correction:
an offset-only executable scan is still too noisy. Numeric displacements such as 0x400 / 0x420
occur in unrelated classes and stack/local layouts. Several high-ranked V7 functions were proven
false positives after disassembly.

Example:
RVA 0x00E21320 is reflection/metadata construction using RBP locals whose offsets coincidentally
equal the GuiInventoryItemData field offsets. It is NOT the runtime resolver.

### Verified GuiInventoryItemData class anchors

Offline disassembly of V7 snippets identified a real GuiInventoryItemData constructor:

- constructor RVA: 0x00C73050
- copy constructor RVA: 0x01A14D70
- related/secondary initializer RVA: 0x00C739A0
- constructor installs vtable RVA: 0x0293C8C0

The copy constructor verifies field widths, which is critical for eliminating false positives:

- +0x130 m_MaxItemLevel = 32-bit
- +0x193 m_CanAffordAlternatePrice = byte
- +0x3F0 m_UpgradeItemLevel = 32-bit
- +0x400 m_HigherLevelBlueprint = 64-bit-like/pointer-sized field
- +0x418 m_CanAffordCraft = byte
- +0x419 m_ShowupgradeInfo = byte
- +0x41A m_IsBlueprint = byte
- +0x41B m_IsBlueprintAvailable = byte
- +0x41C m_IsBlueprintPinned = byte
- +0x41D m_CanPinBlueprint = byte
- +0x41E m_CanUnPinBlueprint = byte
- +0x420 m_HasABlueprintUpgrade = byte

The copy constructor directly copies these fields from source to destination at the offsets above.

### V8 collector

Built:
GH1_PHASE_C_GUIINVENTORY_CLASS_XREF_COLLECTOR_V8.zip
SHA256:
d028173843781d2b59e2ed59f08375c626600a6461edafbb1ba33ccb14fefb03

V8 is class-anchored and type-aware:
- exact DLL SHA guard;
- parses GuiInventoryItemData vtable at RVA 0x0293C8C0 and extracts its code methods;
- finds all direct callers of constructor/copy constructor/secondary initializer;
- scans field accesses using verified field widths;
- strongly ranks functions touching multiple blueprint fields on the same base register;
- prioritizes functions already anchored to the GuiInventoryItemData class;
- extracts one caller and one callee layer around strong candidates;
- read-only; one DLL only; no PAK/save scan.

Do not use V7 rank ordering as resolver evidence.
Use V8 class-anchored output to identify the real population function for
m_HigherLevelBlueprint / m_HasABlueprintUpgrade.


## V8 correction — actual GuiInventoryItemData anchors

User returned:
GH1_PHASE_C_GUIINVENTORY_CLASS_XREF_V8_20261002_182739.zip

The V8 collector worked, but disassembly of its output exposed an important correction:
the initial V8 constructor/vtable seeds inherited from V7 mixed multiple GUI item-data classes.
Do NOT use RVA 0x00C73050 / 0x00C739A0 / vtable 0x0293C8C0 as the canonical
GuiInventoryItemData identity.

Stronger class identity recovered from V8 output:

- actual/default GuiInventoryItemData constructor: RVA 0x018F0EB0
- GuiInventoryItemData copy constructor: RVA 0x01A14D70
- actual GuiInventoryItemData vtable: RVA 0x02B4F330
- generated class size: 0x5E0

Evidence:
- RVA 0x018F0EB0 writes vtable 0x02B4F330 into the object and initializes the complete
  object layout through the 0x5E0 range;
- RVA 0x01A14D70 copies the same field layout and remains the useful copy-constructor anchor;
- V6 generated class registration at RVA 0x007BD3B0 identifies GuiInventoryItemData
  with class size 0x5E0 and field-registration callback RVA 0x00759460.

Important runtime-field offsets remain valid because they came from generated reflection metadata,
not from the incorrect V7/V8 class anchor:
- +0x130 m_MaxItemLevel
- +0x193 m_CanAffordAlternatePrice
- +0x3F0 m_UpgradeItemLevel
- +0x400 m_HigherLevelBlueprint
- +0x418 m_CanAffordCraft
- +0x419 m_ShowupgradeInfo
- +0x41A m_IsBlueprint
- +0x41B m_IsBlueprintAvailable
- +0x420 m_HasABlueprintUpgrade

V8 also produced many direct callers of the actual constructor RVA 0x018F0EB0.
The fact that most callers do not populate +0x400/+0x420 inline indicates that runtime population
is likely delegated into helper calls after construction.

### V9 corrected resolver-graph collector

Built:
GH1_PHASE_C_GUIINVENTORY_RESOLVER_GRAPH_COLLECTOR_V9.zip

ZIP SHA256:
2e0378177b2898bd9493df257b4e99bc100448f2494642ec7d3f6eaecca73e38

Core script SHA256:
e36b7a33b39b4ad71ccee4d2b9c684a0f361be99c577f039f0534ddb6c628174

V9 starts only from the corrected class identity:
- constructor 0x018F0EB0
- copy constructor 0x01A14D70
- vtable 0x02B4F330
- size 0x5E0

V9:
- builds one direct-call index for gamedll;
- finds all direct callers of the corrected ctor/copy ctor;
- parses the corrected vtable;
- follows a bounded 3-hop class-specific call graph;
- scans type-correct accesses to the reflection-proven blueprint fields;
- ranks +0x400 / +0x420 writers much higher when they are connected to the corrected class graph;
- captures caller layers around strong resolver candidates;
- captures generated field-accessor thunks and their callers for semantics;
- one DLL only, mmap/read-only, no PAK/save scan.

Research rule:
Do NOT build a new Legendary->Iconic runtime patch until V9 identifies a credible
post-construction population/resolver function for m_HigherLevelBlueprint and/or
m_HasABlueprintUpgrade.


## V9 result — resolver uses virtual population path; direct 3-hop writer search insufficient

User returned:
GH1_PHASE_C_GUIINVENTORY_RESOLVER_GRAPH_V9_20261002_193959.zip

Verified DLL:
- gamedll_ph_x64_rwdi.dll
- SHA256 ddb68c8f87ba2afd0e561b2d1adb9235467c29069fb1cd1619db81e1056378eb

V9 stats:
- direct call edges: 312,835
- real GuiInventoryItemData ctor callers: 91
- copy-ctor callers: 3
- forward class graph nodes at depth <=3: 853
- type-correct field accesses: 1,453
- critical writer functions detected globally: 99
- extracted functions: 520

Important finding:
After excluding constructor/copy-constructor initialization, V9 did NOT identify a credible
post-construction writer of both m_HigherLevelBlueprint (+0x400) and
m_HasABlueprintUpgrade (+0x420) inside the first three direct-call hops from the corrected
GuiInventoryItemData class seeds.

Several high-ranked global candidates are false positives even after type-width filtering.
For example functions around RVA 0x010BF550 / 0x012F3E00 / 0x012F5F90 initialize unrelated
large structures with float/vector constants at offsets that merely collide with 0x130/0x3F0/0x400.
Do not treat raw V9 ranking alone as resolver evidence.

### Concrete virtual-population discovery

The actual GuiInventoryItemData vtable contains high-value population/update methods.

Most important:
RVA 0x019434B0 (actual vtable slot 106 / byte offset 0x350) is a real GuiInventoryItemData
population/orchestration method.

Disassembly shows it:
- reads the source item pointer from GuiInventoryItemData +0x5B0;
- queries the source item through multiple virtual calls;
- writes GUI fields through dedicated helper/setter functions;
- calls additional workbench/inventory helpers such as 0x0194EE80, 0x01945FB0,
  0x01947CC0, 0x01947130, 0x0194E360, 0x01937630, 0x019467C0 and 0x01947950.

Other relevant actual vtable methods include:
- 0x01940E00
- 0x019425D0
- 0x01942CB0
- 0x01942D80
- 0x019434B0

This explains why the direct-call-only V9 graph did not expose the resolver:
the real path is heavily virtual and also uses split/cold PDATA fragments.

### V10 targeted resolver-slice collector

Built:
GH1_PHASE_C_WORKBENCH_RESOLVER_SLICE_COLLECTOR_V10.zip

SHA256:
2417bcd0eb8c72e458677b264242367c1e7412a6248f85d6f6ff876ee7a99420

V10 scope:
- one DLL only, exact SHA guard;
- seeds only the real GuiInventoryItemData populate/update method family plus
  MenuShopController::UpgradeCurrentBlueprint;
- extracts first 108 actual GuiInventoryItemData vtable slots;
- follows direct CALL + relative JMP/Jcc/cold-fragment targets to depth 5;
- extracts a small contiguous code slice 0x01930000..0x01952000 so split PDATA fragments
  around the workbench GUI path cannot be missed;
- reports +0x400 m_HigherLevelBlueprint and +0x420 m_HasABlueprintUpgrade accesses only
  inside this targeted workbench graph;
- extracts callers of any critical function found;
- read-only; no PAK/save scan.

Research rule remains:
Do NOT create a new runtime Legendary->Iconic patch until the targeted V10 workbench path
shows where the higher-blueprint pointer/flag is populated or rejected.


## V10 result — static virtual graph exhausted; V11 live source-item probe

User returned:
GH1_PHASE_C_WORKBENCH_RESOLVER_SLICE_V10_20261002_195953.zip

Verified DLL:
- gamedll_ph_x64_rwdi.dll
- SHA256 ddb68c8f87ba2afd0e561b2d1adb9235467c29069fb1cd1619db81e1056378eb

V10 stats:
- graph nodes: 674
- graph edges: 4205
- targeted field accesses: 10
- critical +0x400/+0x420 functions: 2
- critical callers: 143
- extracted snippets: 766

### Decisive V10 correction

The apparent targeted +0x400 writer at RVA 0x00D33830 is NOT the blueprint
successor resolver. Disassembly shows it is another large object constructor:
- it initializes a broad contiguous object layout;
- it zeros +0x3F0/+0x400/+0x410/+0x418/+0x420 and many unrelated fields together;
- its +0x400 store is constructor initialization only.

The second +0x400 writer in the targeted result is the already-known
GuiInventoryItemData default constructor RVA 0x018F0EB0, again initialization only.

Therefore V10 still found no credible post-construction direct writer of
m_HigherLevelBlueprint / m_HasABlueprintUpgrade.

### What V10 confirms about the real workbench path

Actual GuiInventoryItemData vtable method RVA 0x019434B0:
- reads the source item pointer at this+0x5B0;
- calls source-item virtual methods at offsets including 0x330, 0x338, 0x348,
  0x360 and 0x370;
- delegates into helpers including 0x0194EE80, 0x01945FB0, 0x01947CC0,
  0x01947130, 0x0194E360, 0x01937630, 0x019467C0 and 0x01947950.

MenuShopController::UpgradeCurrentBlueprint likewise calls source/item virtual
methods and controller helpers rather than exposing a simple direct max-tier
comparison in the extracted static slice.

Conclusion:
the remaining resolver is behind the runtime source-item class/vtable.
Another generic static offset/xref collector would add noise rather than proof.

### V11 — read-only live blueprint object probe

Built:
GH1_PHASE_C_LIVE_BLUEPRINT_OBJECT_PROBE_V11.zip

SHA256:
780256a3013cd08d156fa451e3016b2025746204b724b79f0bcef924c7bd4eca

Purpose:
- run while the game is open at Workbench with the existing Legendary Sunray
  blueprint highlighted;
- find live GuiInventoryItemData instances by the proven vtable RVA 0x02B4F330;
- read only the proven fields:
  +0x130 m_MaxItemLevel
  +0x193 m_CanAffordAlternatePrice
  +0x3F0 m_UpgradeItemLevel
  +0x400 m_HigherLevelBlueprint
  +0x418 m_CanAffordCraft
  +0x419 m_ShowupgradeInfo
  +0x41A m_IsBlueprint
  +0x41B m_IsBlueprintAvailable
  +0x420 m_HasABlueprintUpgrade
  +0x5B0 m_SourceItem
- obtain the actual source-item vtable used by the selected blueprint;
- read only selected virtual-function pointers observed in V10:
  0x2E0, 0x328, 0x330, 0x338, 0x348, 0x360, 0x370,
  0x970, 0xF08, 0x1298, 0x12F8, 0x1550, 0x1568, 0x1580;
- convert function VAs to gamedll RVAs;
- extract only those small on-disk function bodies for offline disassembly.

V11 process access is READ-ONLY:
- PROCESS_QUERY_INFORMATION
- PROCESS_VM_READ
- VirtualQueryEx
- ReadProcessMemory
- no WriteProcessMemory
- no save/PAK/DLL/EXE modification
- no whole-process memory dump.

This probe is useful even if POC9 is not currently installed because the immediate
goal is to identify the exact runtime source-item class and virtual methods used by
the legacy Sunray blueprint. Once those method RVAs are known, inspect the actual
successor/max-tier resolver rather than generic GUI code.

Research rule:
Do not build another Legendary->Iconic runtime patch until V11 maps the source-item
virtual functions and the actual successor/max-tier decision path.


## V11 / V11.1 / V12 / V12.1 / V12.2 runtime probe results — exact Workbench class proven

### V11 result — zero due scan cap, not negative runtime proof

User returned:
GH1_PHASE_C_LIVE_BLUEPRINT_OBJECT_V11_20261002_221433.zip

Result:
- RAW_CANDIDATES=0
- VALIDATED_LATEST=0
- memory scan stopped exactly at 4 GiB hard cap
- DLL SHA and module base were correct

Interpretation:
V11 did not prove absence of GuiInventoryItemData. The address-order 4 GiB cap exhausted
before reaching the relevant heap.

### V11.1 result — base class live scan GREEN

V11.1 changed scan order to enumerate the full memory map and prioritize writable
MEM_PRIVATE regions.

Runtime result:
- 378 live objects using the base GuiInventoryItemData vtable were found
- approximately 14.2 GiB of prioritized readable heap was scanned
- live process-memory reading itself is therefore proven operational
- the objects were base GuiInventoryItemData objects, not the derived Workbench class

Important correction:
Workbench uses derived GuiShopItemData; scanning only the base vtable cannot identify
the Workbench upgrade gates reliably.

### GuiShopItemData structure correction

V6 reflection metadata plus V10/V12 disassembly establish:
- GuiInventoryItemData class size = 0x5E0
- GuiShopItemData class size = 0x958
- actual GuiShopItemData constructor RVA = 0x018F4F50
- base GuiInventoryItemData constructor RVA = 0x018F0EB0
- primary GuiShopItemData vtable RVA = 0x02B65D50

Constructor proof:
- ctor+0x0D CALL resolves to base ctor 0x018F0EB0
- ctor+0x1D LEA resolves to primary vtable 0x02B65D50
- constructor initializes Workbench-derived fields including +0x5F4 and +0x600

GuiShopItemData Workbench fields:
- +0x5F1 m_CanCraft
- +0x5F2 m_CanEnhance
- +0x5F3 m_ShowEnhance
- +0x5F4 m_CanUpgrade
- +0x5F5 m_ShowCraft
- +0x5F6 m_ShowUpgrade
- +0x5F7 m_IsBlueprintUpgrade
- +0x600 m_LowerLevelBlueprint

### V12 / V12.1 — rejected discovery attempts

V12 initially crashed before heap scan because the collector omitted the Python
defaultdict import. V12.1 fixed that crash but its generic factory heuristic chose
the wrong constructor candidate 0x005E8680 instead of the real 0x018F4F50.
The four V12.1 objects with nonsensical field values are false targets and must not
be used as runtime evidence.

### V12.2 — exact GuiShopItemData live probe GREEN

User returned:
GH1_PHASE_C_LIVE_GUISHOP_EXACT_V12_2_20261002_225156.zip

Verified:
- DLL SHA256 ddb68c8f87ba2afd0e561b2d1adb9235467c29069fb1cd1619db81e1056378eb
- exact ctor RVA 0x018F4F50
- exact primary vtable RVA 0x02B65D50
- first 16 vtable entries all point inside gamedll
- exact-vtable heap candidates: 333
- latest valid GuiShopItemData objects: 333
- blueprint flag = 1 on 254 objects
- HasABlueprintUpgrade = 1 on 90 objects
- ShowUpgrade = 1 on 1 object
- CanUpgrade = 1 on 0 objects
- IsBlueprintUpgrade = 1 on 0 objects
- source-method rows: 1512
- approximately 14.3 GiB process memory read

Runtime population split:
- 90 live blueprint objects have HasABlueprintUpgrade=1 and a non-null
  m_HigherLevelBlueprint pointer
- 33 live blueprint objects have MaxItemLevel=3, HasABlueprintUpgrade=0 and
  m_HigherLevelBlueprint=null
- those 33 rows collapse to 13 unique source-item objects

This is direct runtime proof that the engine genuinely distinguishes blueprint
objects with a resolved successor from terminal generated T3/max=3 blueprint
objects. The legacy blocker is therefore not merely a hidden GUI button.

Do NOT yet claim that a specific one of those 13 terminal source objects is Sunray.
V12.2 did not map source-item identity/name back to the generated Sunray T3 ID.

### V13 — exact Sunray identity probe

Built:
GH1_PHASE_C_LIVE_SUNRAY_IDENTITY_PROBE_V13.zip

SHA256:
c68cbeea55658a244030c267a87bd88aa2c3fc08ed11090525b48abede9eaacd

Purpose:
- reuse the exact proven GuiShopItemData vtable;
- collect live m_SourceItem pointers;
- search process memory for exact Sunray/generated identifiers:
  Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T3_Blueprint,
  T2, T1, family dlc_ft_firearm_revolver_c_legendary_r, and Sunray;
- map exact string identity back to source item by inline text / direct pointer /
  bounded one- and two-hop pointer traversal;
- report the exact Workbench gates only for the source object(s) tied to Sunray.

Research rule:
Do not patch DLL/runtime state and do not scale any legacy migration mechanism until
V13 identifies the exact Sunray source item and confirms its live gate tuple.


## V13 result — exact IDs present; bounded identity walk did not reach m_SourceItem

User returned:
GH1_PHASE_C_LIVE_SUNRAY_IDENTITY_V13_20261002_230250.zip

Verified runtime:
- same process PID 33356 as V12.2
- same gamedll SHA256 ddb68c8f87ba2afd0e561b2d1adb9235467c29069fb1cd1619db81e1056378eb
- exact GuiShop objects: 333
- unique m_SourceItem objects: 186
- identity-matched source objects: 0
- matched GuiShop objects: 0

This is NOT a missing-identity result. Exact Sunray/generated strings were present live:
- Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T3_Blueprint: 5 ASCII hits
- T2 ID: 5 ASCII hits
- T1 ID: 21 ASCII hits
- family dlc_ft_firearm_revolver_c_legendary_r: 56 ASCII hits
- Sunray: 5 UTF-16LE hits

Interpretation:
V13's bounded source-item traversal (inline/direct pointer + one/two pointer hops)
did not reach those strings. The live identity is therefore likely behind a deeper
definition/hash/registry topology. Do not interpret this as evidence that Sunray is
not one of the 13 terminal T3 source objects.

Do not increase arbitrary pointer depth blindly; that would explode the graph and
reduce evidence quality.

### V14 — A/B/A selection differential identity probe

Built:
GH1_PHASE_C_SUNRAY_SELECTION_DIFF_PROBE_V14.zip

SHA256:
e84efb1f05bcc01dbab2572b59042859eaaeb00db1e3586c1fa3df9a55ea8853

Method:
- derive the 13 terminal generated-T3 source groups fresh from exact GuiShopItemData
  runtime objects;
- track qword references to BOTH each terminal m_SourceItem pointer and each
  GuiShopItemData object pointer belonging to that source;
- Stage A: existing Legendary Sunray highlighted;
- Stage B: user highlights a clearly different/non-Sunray blueprint;
- Stage A2: user returns highlight to the same Legendary Sunray;
- rank source groups by references present in both Sunray stages, absent in the
  other-selection stage.

This avoids any assumption about string/hash/definition layout and remains strictly
read-only (QUERY_INFORMATION + VM_READ; no WriteProcessMemory).

If V14 yields one stable A-only source/object reference signature, use that source
as the runtime Sunray identity and read its V12.2-proven gate tuple directly.
If V14 yields no unique signature, selection is likely held through another controller
object; next step should follow that controller reference rather than deeper blind
identity-string pointer walking.
