# GH1 Phase B Global V1 — Weapon + Matching Blueprint

Date: 2026-10-01

## Baseline
GH1 Phase A remains runtime GREEN:
- universal weapon dismantle: PROVEN
- universal outfit dismantle: PROVEN
- universal weapon drop: PROVEN
- universal outfit drop: PROVEN

GH1 includes the current installed stack, including Survivor Sense/XRay.

## POC3 runtime result — REJECTED ROUTE
User tested the prior ordinary-Biter POC3 for more than ~500 zombie kills and did not observe the intended weapon+blueprint pair. Firearm presence also did not appear meaningfully changed.

POC3 had patched the vanilla-style `lootpools_ft.loot` / `lootsets_ft.loot` route. Current GH1 audit instead shows the effective project loot chain is the global custom layer:

`default.loot` -> `tbp_lootpools_global_v1.loot` -> `tbp_lootsets_global_v1.loot`

This is the same GH1 layer that carries the current resource/high-loot/G1/charm/Night Sovereign logic.

### New locked loot rule
For this project, new zombie loot-pool features must be integrated into the current GLOBAL `tbp_*` layer unless a different route is independently proven.

Do not continue Phase B by patching isolated vanilla `LootedObject` routes.

## User-requested Phase B semantics
Blueprint acquisition is scoped to zombie loot:
- if an infected corpse yields a weapon through the GH1 project weapon route,
- the same loot reward must also provide the matching weapon blueprint,
- owning the weapon from stash/trader/other sources must not globally trigger blueprint acquisition.

Example intent: a sniper/Goldrush-class weapon obtained from a zombie should come with the corresponding blueprint.

## Pairing mechanism
Use an `ItemBundle` containing:
1. exact selected weapon rank item;
2. matching T1 weapon blueprint.

Reason:
- current GH1 already contains a working `Night_Sovereign_Set_Bundle` using `CategoryType_ItemBundle` + `BundleItems()` to grant multiple items together;
- historical GH1 project state records `DLTB_PlayNow_AllAmmoBlueprints` as a one-bundle drop containing six craftplans.

This is preferred over mass-editing weapon definitions. Phase B POC1 mass `LinkedItems` remains HARD REJECTED after inventory/stash/weapon identity corruption.

## Blueprint source policy
For every weapon family present in the current GH1 global weapon pools:

1. If current game data already provides a native weapon blueprint, use it.
2. If no native weapon blueprint is found, generate a clean current-version T1/T2/T3 chain from current weapon metadata.

The generated chain follows the structure learned from the user-supplied Nexus mod 686 reference only; the old mod file itself is not installed:
- `CraftplanType("Weapon")`
- `ScaleWithPlayerRank("<family>_r")`
- T1 `Color_Blue`
- T2 `Color_Violet`
- T3 `Color_Orange`
- `ItemLevel()`
- `NextLevelBlueprintName()`
- native upgrade-component price pattern for T2/T3.

Nexus 686 is treated as a design/reference source, not a current-version payload.

## Global V1 implementation
Artifact:
`GH1_PHASE_B_GLOBAL_WEAPON_BLUEPRINT_V1_READY.zip`

Artifact SHA256:
`3d72ac11e93ce6f9406732f03280d57c00d08810bdb2fc56661add302c0c7127`

Installer behavior:
- if exact POC3 is still installed, auto-rollback it to exact Phase A GREEN first;
- validate Phase A state/hash;
- read current effective files from installed PAKs;
- patch only the current global GH1 loot layer plus current `collectables_ft.scr`;
- preserve current data4 Sense and Phase A files;
- back up exact Phase A data4 before installing.

Target global weapon pools:
- `DLTB_PlayNow_Firearm_Common`
- `DLTB_PlayNow_Firearm_Rare`
- `DLTB_PlayNow_Firearm_Epic`
- `DLTB_PlayNow_Firearm_Legendary`
- `DLTB_G1_Firearm_ExoticNative`
- `DLTB_PlayNow_Melee_Common`
- `DLTB_PlayNow_Melee_Rare`
- `DLTB_PlayNow_Melee_Epic`
- `DLTB_PlayNow_Melee_Legendary`

Target infected objects:
- Biter
- Biter_Police
- Viral
- Screamer
- Spitter
- Banshee
- Hag
- Suicider
- Charger
- Goon
- Demolisher
- Corruptor
- Bolter
- Volatile
- Volatile_Apex
- Tyrant

The existing GH1 project weapon-route weights/min/max are preserved while route names are replaced by paired bundle pools.

`Enemy_Lottery_Weapons` is disabled only inside these infected blocks to prevent an unpaired fallback weapon drop.

## Static verification against audited current GH1
Parsed current global lootsets:
- Firearm Common: 4 families / 60 rank entries
- Firearm Rare: 8 / 120
- Firearm Epic: 4 / 60
- Firearm Legendary: 11 / 165
- G1 ExoticNative: 21 / 315
- Melee Common: 4 / 60
- Melee Rare: 62 / 916
- Melee Epic: 2 / 30
- Melee Legendary: 21 / 315

Unique family union: 137.

Static global-pool patch simulation:
- all 16 target infected `LootedObject` blocks matched and changed;
- all nine target project weapon pools had live calls in infected routes;
- `Enemy_Lottery_Weapons` zeroing matched;
- generated paired global lootset definitions passed structural tests;
- generated blueprint + ItemBundle collectables injection passed synthetic structural test;
- Python installer compile passed;
- ZIP integrity passed.

## TEST-PENDING — do not call GREEN yet
Runtime proof is still required for:
1. zombie project weapon drop produces weapon + matching blueprint together;
2. blueprint unlock/add works;
3. blueprint persists through save/reload;
4. weapon identity and stats remain normal;
5. current rarity behavior is preserved when weapon is delivered through the bundle;
6. stash and existing weapons remain normal;
7. Phase A Drop/Dismantle remains GREEN;
8. GH1 Sense/XRay remains functional;
9. current resource/charm/Night Sovereign behavior remains intact.

### Important rarity caveat
The ItemBundle route guarantees pairing by design, but whether the outer GH1 `ColorSet(...)` continues to influence the weapon contained inside the bundle is not yet runtime-proven. Do not claim rarity preservation until tested.

## Deferred Phase B progression
Not implemented in Global V1:
- Exotic blueprint tier
- Iconic blueprint tier
- post-level-15 Legend scaling / Legend 1–300 progression

Those are the next Phase B steps only after the global weapon+blueprint pairing layer is runtime GREEN.
