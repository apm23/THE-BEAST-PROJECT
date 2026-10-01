# THE BEAST PROJECT — GH1 EXPANSION MASTER STATE

Date: 2026-10-01
Status: ACTIVE AUTHORITATIVE ADDENDUM

This file extends, but does not rewrite, the older SP1/Sense history. For the exact currently-installed mod stack, `MASTER_INSTALLED_MOD_MANIFEST_2026-10-01.md` remains the source of truth.

## 1. GH1 ALIAS

**GH1** is the user's shorthand for the **entire mod stack currently installed in Dying Light: The Beast**, including Survivor Sense / XRay.

When the user says `GH1`, interpret it as the current installed stack recorded in `MASTER_INSTALLED_MOD_MANIFEST_2026-10-01.md`, not as an older historical package such as USER_HIGH_LOOT_SPECIAL45 alone.

GH1 currently includes, among other installed functions:
- inventory-capacity expansion,
- custom XP-farm armor/outfit tuning,
- resource/high-loot/G1/SPECIAL45 merged loot,
- JovianStone flashlight changes,
- Syxsta silent/reduced-noise firearms,
- G1 Night Sovereign / charms,
- older broad AI/Sense edits,
- native Biter Survivor Sense/XRay route,
- the currently installed Sense V2 overlay.

### Sense status inside GH1
Runtime-GREEN / proven:
- ordinary Biters are highlighted through walls by native Survivor Sense,
- sleeping/resting Biters are also highlighted,
- proven mechanism is the empty-key hostile fallback in `survivor_sense_hostility_presets.scr`.

Installed but still TEST-PENDING:
- cyan Biter presentation from V2,
- near-instant fade tuning,
- extended turn-away / long-distance persistence tuning.

Do not upgrade TEST-PENDING Sense items to GREEN unless the user explicitly reports success.

## 2. DEVELOPMENT CONTRACT — ONE FEATURE AT A TIME

The user explicitly does **not** want a total GH1 compile yet.

Mandatory workflow for every new gameplay feature:
1. Freeze GH1 as the baseline.
2. Build exactly one isolated/reversible test feature on top of GH1.
3. User performs runtime test.
4. Only after explicit user confirmation, mark that feature PROVEN/GREEN and lock it into master state.
5. Move to the next feature.
6. Do not consolidate everything while any requested feature remains unproven.
7. After all requested features are GREEN, user will reinstall DLTB fresh and the project may build one consolidated reinstall bundle.
8. Only after the single-player consolidated baseline is stable, continue the CO-OP branch.

A failed feature test must not invalidate or overwrite the GH1 baseline.

## 3. NEW GH1 EXPANSION GOALS

### Phase A — Universal player weapon + outfit drop/dismantle
Status: **TEST-PENDING / POC1 BUILT**

Goal:
- all normal player-facing weapon classes should be droppable and dismantleable,
- all normal player-facing clothing/outfit parts should be droppable and dismantleable,
- include named/event/rarity variants where they are genuine player inventory items,
- exclude AI-only attack proxies, invisible/internal items, ammo/projectile internals, and quest-critical/internal proxy items unless separately tested later.

Safety rules:
- use existing native `CanDrop` and `DismantleResult` systems,
- use existing native dismantle routes only,
- do not structurally rewrite `LootedObject` topology,
- do not touch loot frequency, GH1 resource balance, Sense, flashlight, firearm sound/noise, armor stats, save/versioning, or inventory capacity,
- test package must be reversible and preserve the exact pre-test GH1 state.

Known native dismantle route families already verified in game data:
- `Dismantle_T1/T2/T3_Slash`
- `Dismantle_T1/T2/T3_Blunt`
- `Dismantle_T1/T2/T3_Firearm`
- `Dismantle_T1/T2/T3_Ranged`
- `Dismantle_Charm_Mod`

For outfit parts there is no dedicated outfit dismantle route confirmed in the current research set. POC1 therefore uses native `Dismantle_T1_Blunt` as the conservative outfit fallback because its native result is low-tier Scrap and it requires no new LootedObject topology.

### Phase B — Any obtained weapon also unlocks/links its weapon blueprint
Status: PLANNED / NOT PROVEN

Goal:
- weapon acquisition should provide/unlock the corresponding weapon blueprint,
- preserve weapon identity rather than convert everything to one generic weapon,
- prefer native `LinkedItems`, CraftPlan, docket and blueprint chains where available.

Native evidence already identified:
- player weapon definitions can use `LinkedItems("Craftplan_..._T1_Blueprint")`,
- native weapon blueprint chains use `CraftplanType("Weapon")`, `ScaleWithPlayerRank(...)`, `ItemLevel(...)`, and `NextLevelBlueprintName(...)`.

Do not implement this phase until Phase A is runtime-GREEN.

### Phase C — Upgradeable weapon blueprint progression through Exotic/Iconic and Legend progression
Status: PLANNED / NOT PROVEN

Goal:
- blueprint progression should raise native weapon stats with level/tier,
- progression should reach Exotic/Iconic using the game's actual native rarity/quality mechanisms, not cosmetic recoloring,
- after normal level/rank 15, progression should continue through Legend progression,
- target upper Legend progression currently planned as **Legend Level 300**, but exact engine linkage/scaling must be verified during this phase before implementation.

Important historical rule:
- genuine native generated weapon state/persistence is preferred,
- the old temporary custom CraftPart magnitude approach for Ascension did not persist correctly and must not be reused.

### Phase D — Custom Exotic charm with special stats
Status: PLANNED / NOT PROVEN

Goal:
- create one or more custom charms using the native charm/crafting-effect system,
- rarity target: Exotic,
- special stat effects must be backed by native effect/stat mechanisms wherever possible,
- save/reload persistence must be verified before GREEN.

Existing GH1 already contains native/custom G1 charm routes and therefore provides a base architecture.

### Phase E — Raise charm drop prominence above ordinary resources
Status: PLANNED / NOT PROVEN

Goal:
- charm drops should be more prominent than common resource drops such as Scrap,
- reuse the existing GH1 `DLTB_G1_Charms` branch where possible,
- preserve corpse interaction and existing LootedObject topology,
- do not accidentally increase or destroy unrelated resource/weapon routes.

### Phase F — Standalone noclip/fly toggle
Status: PLANNED / NOT PROVEN / **MUST REMAIN SEPARATE**

Goal:
- toggleable flight/noclip,
- pass through walls/rooms for faster progression/testing,
- toggle OFF restores normal movement/collision.

This module must be developed separately from the main GH1 gameplay expansion so failure cannot damage inventory, loot, armor, weapon progression, Sense, or save behavior.

## 4. FINALIZATION ORDER

Only after Phases A-E are individually runtime-GREEN:
1. freeze every proven feature and exact hashes,
2. prepare final GH1 successor manifest,
3. user performs a fresh DLTB reinstall,
4. build/install one consolidated single-player reinstall bundle,
5. smoke-test all proven functions together,
6. then resume CO-OP/MultiMod integration.

Phase F noclip remains a standalone optional module even after the main consolidated package exists, unless the user explicitly changes that requirement.

## 5. CURRENT NEXT SAFE ACTION

**Runtime-test Phase A POC1.**

Do not start Phase B and do not mark Phase A GREEN until the user reports runtime results for weapon Drop, weapon Dismantle, outfit Drop and outfit Dismantle.

## 6. PHASE A POC1 BUILD RECORD

Artifact name:
`GH1_FEATURE_A_UNIVERSAL_DROP_DISMANTLE_POC1_READY.zip`

Artifact SHA256:
`a7ceb5b19282c03d4a6ccf86ae06e34e4d958fdc87c537d51676ed04bc9093f3`

Build architecture:
- runtime one-click builder; no final binary PAK stored in repo,
- exact GH1 hash gate for current `data2.pak`, `data3.pak`, and `data4.pak`,
- backup exact pre-test `data4.pak`,
- read effective inventory scripts across `data0 -> data4`,
- preserve current data4/Sense payload and overlay only changed inventory scripts into test data4,
- do not modify `data2.pak` or `data3.pak`,
- exclude inventory versioning, AI-only/invisible/internal items and known quest/tutorial/debug/test placeholders,
- player-facing melee/firearm/outfit items receive `CanDrop(true)` where needed,
- empty/missing player-item dismantle routes receive existing native Slash/Blunt/Firearm/Ranged route based on type/tier,
- current inherited shotgun/bow/crossbow/harpoon definitions with empty dismantle routes are patched to native Firearm/Ranged dismantle routes,
- outfit fallback is native `Dismantle_T1_Blunt` (low-tier Scrap-only route),
- uninstall restores exact pre-test data4 only when installed test hash still matches; otherwise STOP SAFE.

Static validation before handoff:
- Python compile PASS,
- current GH1 `inventory_outfits_ft.scr`: 108 targeted outfit blocks patched in dry static pass, all 108 empty dismantle routes removed and 102 explicit `CanDrop(false)` removed,
- current GH1 `inventory_weapondefintions.scr`: all 28 known empty inherited weapon dismantle routes classified/patched in dry static pass,
- no runtime success claim yet.
