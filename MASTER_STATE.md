# MASTER_STATE

## Authority

This file plus actual GitHub HEAD are authoritative for continuation. Reconcile both before acting.

Continuity phrase:

`BEAST-PROVEN-SWITCH45`

Interpret it as: continue THE BEAST PROJECT from this exact state, preserve proven runtime structures, and do not restart rejected experiments.

## Baseline

- Game: **Dying Light: The Beast**
- Target build: **VER. 1.71E**
- Steam AppID: **3008130**
- Fresh-install baseline captured before mod development.
- Clean save remains local/private and must not be committed.
- Clean archive map: `data0.pak,data1.pak`.
- Targeted 1.71E extraction completed locally: **58 requested files, 0 missing**.
- Repository must contain only tooling/docs/config/audit state. Do **not** commit proprietary PAKs, vanilla extracted archives, saves, DLLs, EXEs, or local binary distributions.

## Current phase

**CURRENT RUNTIME-GREEN PLAY STATE:** the project has moved past the old A1+A2+A3 V3 experiment. The current proven architecture is **A1+A2 loot in `data2.pak` + vanilla output-only recipe overrides in `data3.pak`**, with a one-click installer/uninstaller and a proven NORMAL <-> CO-OP MultiMod switcher.

The user's current canonical gameplay profile is **USER HIGH LOOT SPECIAL45**.

Important current status:

- Corpse `F` interaction: **runtime GREEN** on the frozen corpse-safe lineage.
- DLC behavior: **runtime GREEN** on the current lineage; no DLC-disabled popup in proven builds.
- `data2` / `data3` split: **runtime GREEN**.
- One-click install / uninstall / detect architecture: **GREEN enough for continued use**.
- CO-OP MultiMod mode: **RUNTIME PROVEN**; user successfully joined sibling's vanilla world while user remained modded.
- Sibling does not currently want the gameplay mod installed.
- A3 inventory expansion is **SUSPENDED** and must not be reintroduced unless explicitly requested.
- Manual Save Anywhere remains **PAUSED / CLOSED TEMPORARILY** by user decision.
- POC-001 and POC-002 remain frozen green.
- POC-003 arbitrary custom L+1 parameter-magnitude strategy remains rejected after uninstall testing.
- Deeper Legendary Core + uninstall-persistent per-item Ascension is still not implemented.

## Hard safety rules

Priority order:

1. Save / DLC safety.
2. Corpse loot interaction must remain functional (`F`).
3. Preserve runtime-proven structures.
4. Prefer numeric balance changes over structural rewrites.
5. Keep install / rollback simple and detectable.
6. Preserve CO-OP with vanilla sibling.

Do **not** reintroduce or casually modify:

- A3 inventory expansion;
- `player_variables`;
- `stash_dlc`;
- inventory versioning;
- quickslot/stash rewrites;
- save-versioning paths;
- DLC-sensitive files;
- aggressive `LootedObject` structure replacement;
- delete/reorder/add corpse branches without a separately proven need;
- `VisibleQuickSlotsCount` / invented SLOT5-SLOT8 behavior.

Historical hard failure: an aggressive rewrite of `scripts/inventory/loot/lootpools_ft.loot` caused the corpse loot prompt `F` to disappear. Therefore the **`LootedObject` structure is frozen**.

Preferred future balance changes:

- numeric weights;
- existing sub-pool contents;
- min/max quantities;
- isolated safe sub-pools already following the proven structure.

## Frozen project goals

1. Universal native Legendary eligibility even for weapons vanilla-capped at Rare/Epic.
2. Per-weapon rarity gacha while preserving farming/RNG.
3. Increased but controllable weapon availability from infected/humans/supported loot sources.
4. Human held weapon behavior remains separate from extra corpse-loot rolls.
5. Legendary must be real item quality/state, not cosmetic recolor.
6. Legendary Core: Rare/Epic -> Legendary, Legendary -> per-item Ascension.
7. Ascension: L -> L+1 -> L+2 -> L+3 -> L+4 -> L+5.
8. Ascension emphasizes damage/durability; secondary stats moderate; attack speed conservative.
9. Prefer per-item serialized progression, not global definition-only buffs.
10. Preserve weapon identity/model/class.
11. Keep RNG/farming in the final design.
12. Manual Save Anywhere remains a project idea but is **PAUSED** until explicitly reopened.

## Confirmed 1.71E mapping

See `docs/BASELINE_1.71E_MAPPING.md`.

- Blue = Rare; Violet = Epic; Orange = Legendary; Platinum/Exotic exist above Orange.
- Native Legendary generation uses class-specific Legendary affix groups plus `Weapons_Random_Legendary_ft`.
- Lower-rarity weapons can hardcode Rare affix groups; Universal Legendary cannot be cosmetic-only.
- Standard inspected human weapon presets use held-weapon `LootChance(1.0)`.
- `StartupMod(...)` is a confirmed native generation mechanism used by vanilla generated weapons.
- Direct loose `CategoryType_CraftPart` delivery through ordinary Biter corpse-resource loot is rejected as a test-delivery path after runtime failure.

---

# Current proven gameplay lineage

## CORPSE SAFE A1+A2 — runtime GREEN structural baseline

Local artifact:

`DLTB_V3_CORPSE_SAFE_A1_A2.zip`

Package SHA-256:

`b867bcf6b5eca93a91f6535358c1ea84239e4146711687f8f50b3998a5d0cf6f`

`data2.pak` SHA-256:

`dc7dc7970088f7a4f3e7c547c0a6fb7229abaadca8a30f3836491e4624015c75`

Runtime result:

- corpse `F` works;
- DLC normal;
- mod active.

This is the structural safety ancestor. Preserve its corpse-routing topology.

## GREEN BALANCED baseline

Local artifact:

`DLTB_V3_GREEN_BALANCED.zip`

Package SHA-256:

`a7f02823958e09b2d2b2111a81870fc98ea2ae37adeccc37338b47c0dce35ced`

`data2.pak` SHA-256:

`ecbbbc1ca3725c4507ce6e3f893c5e3438dc882e1a4bd4b69dbff4457812609e`

This was built strictly from the runtime-GREEN corpse-safe base and became the main low-loot balance reference.

Relevant GREEN-era balance decisions:

- firearm/melee Common/Rare/Epic project weights strongly reduced from earlier aggressive levels;
- firearm/melee Legendary project weights reduced even more;
- weapon-mod blueprint pressure reduced;
- ammo blueprint pack kept rare;
- native firearm Legendary preference reduced from the older aggressive value;
- corpse structure remained frozen.

---

# A1 — custom standard firearm ammo economy

Six project-authored standard firearm ammo recipes remain active:

- Pistol: `10 Scrap -> 60`
- Revolver: `14 Scrap -> 24`
- SMG: `18 Scrap -> 120`
- Shotgun: `24 Scrap -> 24`
- Rifle: `30 Scrap -> 80`
- Marksman: `37 Scrap -> 32`

## Six-blueprint bundle

The six custom ammo craftplans are delivered as one bundle item:

`DLTB_PlayNow_AllAmmoBlueprints`

Bundle contents:

- `Craftplan_PlayNow_Ammo_Pistol`
- `Craftplan_PlayNow_Ammo_SMG`
- `Craftplan_PlayNow_Ammo_Rifle`
- `Craftplan_PlayNow_Ammo_Shotgun`
- `Craftplan_PlayNow_Ammo_Revolver`
- `Craftplan_PlayNow_Ammo_Marksman`

**One bundle drop = all six custom ammo craftplans.**

Do not split these back into six independent blueprint drops unless explicitly requested.

---

# Vanilla special-ammo recipe patch — proven `data3` architecture

Final architecture:

- `data2.pak` = loot + A1/A2 gameplay mod.
- `data3.pak` = vanilla recipe **output-only** overrides.

`data3` is generated from the user's currently installed official `data0.pak` / `data1.pak` instead of redistributing stale vanilla source.

Current outputs:

- Arrow = `35`
- Fire Arrow = `35`
- Shock Arrow = `35`
- Bolt = `35`
- Fire Bolt = `35`
- Shock Bolt = `35`
- 40mm Electric = `35`
- 40mm Explosive = `35`
- 40mm Flashbang = `35`
- 40mm Freeze = `35`
- 40mm Incendiary = `35`
- Sawblade = `35`
- Flamethrower ammo = `400`

**RequiredItem ingredients remain vanilla.** Do not change special-ammo ingredients unless explicitly requested.

Relevant vanilla craftplans:

- `Craftplan_Arrows_FT`
- `Craftplan_Arrows_Fire_FT`
- `Craftplan_Arrows_Shock_FT`
- `Craftplan_Bolt_FT`
- `Craftplan_Bolts_Fire_FT`
- `Craftplan_Bolts_Shock_FT`
- `Craftplan_GrenadeLauncher_Ammo_Electric_FT`
- `Craftplan_GrenadeLauncher_Ammo_Explosive_FT`
- `Craftplan_GrenadeLauncher_Ammo_Flashbang_FT`
- `Craftplan_GrenadeLauncher_Ammo_Freeze_FT`
- `Craftplan_GrenadeLauncher_Ammo_Incendiary_FT`
- `Craftplan_SawbladeLauncher_Ammo_FT`
- `Craftplan_Flamethrower_Ammo_FT`

Proven source path for these definitions:

`scripts/inventory/collectables_ft.scr`

---

# Final current resource balance

Important correction from an earlier typo:

**Resource chance / route weight is NOT +40%.**

Current rule:

- resource route chance stays at the proven GREEN-style balance;
- when a resource route is selected, the **quantity** is enlarged;
- preserve each material's existing internal relative weight;
- Scrap keeps the already-proven `40++` style ranges.

Typical Scrap ranges retained from the proven lineage include:

- `40-55`
- `45-65`
- `50-70`
- `55-80`

Non-Scrap enemy resource quantity targets:

- Base / Biter / medicine: `33-50`
- Viral / Human: `33-60`
- Screamer: `33-70`
- Screamer Perma: `40-70`
- Charger / Goon: `40-70`
- Volatile: `45-75`
- Baron / elite: `45-80`

Existing materials affected by quantity scaling include resource-pool entries such as:

- Rags;
- Wiring;
- Container;
- Resin;
- Blades;
- Weights;
- Feathers;
- Leather;
- Battery;
- Cleaning Supplies;
- Oxidizer;
- Alcohol;
- Fuel Can;
- other existing `Craft_*` entries in the selected enemy resource pools.

Do not convert this back into an independent +40% resource-chance system.

---

# Two gameplay profiles

## SIBLING BALANCED

Purpose: more conservative weapon pressure.

- firearm + melee project drop weights: approximately **GREEN x1.05**;
- weapon-mod blueprint weights: approximately **GREEN x1.05**;
- native Legendary preference remains conservative relative to old SAFE;
- resource chance = current proven baseline;
- resource quantity = current `33++` / Scrap `40++` system;
- Special Infected Legendary rule below still applies.

Canonical local artifact:

`DLTB_ONECLICK_SIBLING_BALANCED_SPECIAL45.zip`

`data2.pak` SHA-256:

`ab18b545bffbee00ff8ff8ee1e0a9b241bfb2f5864aa88bedc282dab428e771d`

Package SHA-256:

`4e7013a60c10acadaa98a04af78205333cfc86796572227d99d78ebc3c5311b6`

Current usage: sibling ultimately declined installing the gameplay mod, so keep this as an optional artifact only.

## USER HIGH LOOT — current canonical user profile

Purpose: weapon availability close to old A1+A2 SAFE while retaining the safer final architecture.

- firearm + melee project weights = approximately **97% of old A1+A2 SAFE values**;
- native firearm Legendary preference target = `3.88` versus old SAFE `4.0`;
- weapon-mod blueprint weights remain modest at approximately **GREEN x1.05**;
- resource chance = current proven baseline;
- resource quantity = current `33++` / Scrap `40++` system;
- Special Infected Legendary rule below applies.

Canonical local artifact:

`DLTB_ONECLICK_USER_HIGH_LOOT_SPECIAL45.zip`

`data2.pak` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Package SHA-256:

`780ce15ce103febee1f9ebd3d35a272c3635e8683f07f404b4f9094b9890429c`

This is the gameplay payload used by the current CO-OP/NORMAL switcher.

---

# Special Infected Legendary 45% — current rule

Special Infected currently tuned:

- Screamer
- Spitter
- Banshee
- Suicider
- Charger
- Goon
- Demolisher
- Volatile
- Volatile Apex (`Volatile_Apex`)
- Tyrant

**Viral is intentionally excluded** because it is too common and would flood Legendary loot.

Current rule:

When the existing project weapon rarity route is selected for one of the Special Infected above, **Legendary rarity share is 45%**.

More precisely:

- Firearm Legendary + Melee Legendary combined = `45%` of the existing project-weapon rarity weight for that Special Infected;
- Common/Rare/Epic share the remaining `55%` while preserving their prior relative ratio;
- total project-weapon route weight is preserved;
- resource chance is unchanged;
- no new loot branch is added;
- both NORMAL and PERMA routes are tuned.

Important semantic rule:

**This is NOT an absolute 45% Legendary drop chance per kill.** It is a 45% Legendary share **inside the existing project weapon rarity selection** when that weapon route is actually selected.

This implementation deliberately avoids changing `LootAmount`, `LootedObject` topology, or corpse branch structure.

---

# One-click installer architecture

Current installer philosophy:

`DETECT -> verify known hashes -> backup save -> build recipe data3 from official data0/data1 -> install data2 -> install data3 -> verify -> show final status`

Unknown `data2` / `data3`:

**STOP SAFE.** Do not overwrite or delete unknown mod files.

Uninstall philosophy:

`DETECT -> verify exact known project hashes/state -> remove project data2 + data3 -> verify CLEAN`

Do not blindly delete unknown PAKs.

The installer/uninstaller must keep user-facing `.cmd` launchers, explicit status output, and `pause` on success/failure.

---

# CO-OP / MultiMod mode — RUNTIME PROVEN

Goal:

- user remains modded;
- sibling remains vanilla;
- user can join sibling's world.

External compatibility layer used:

Data Pak Limit Bypass / MultiMod.

The project does **not** commit or bundle third-party loader DLL/EXE binaries.

## Current switcher artifact

Local artifact:

`DLTB_USER_SPECIAL45_MODE_SWITCHER.zip`

Switcher package SHA-256:

`55f20cdc44dda8ad9c79d0d1671bf302ee7a0b1410adbb9bba36bb02d5ed28e7`

Gameplay payload inside switcher:

`data2.pak` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

## NORMAL / PROVEN mode

Project gameplay files live at:

- `ph_ft\source\data2.pak`
- `ph_ft\source\data3.pak`

Expected detector state:

`MODE=NORMAL_SOURCE`

User command:

`2_SWITCH_BACK_NORMAL_PROVEN.cmd`

## CO-OP / MULTIMOD mode

Project gameplay files live at:

- `ph_ft\MultiMod\data2.pak`
- `ph_ft\MultiMod\data3.pak`

Project copies in `ph_ft\source\data2.pak` and `ph_ft\source\data3.pak` are removed while CO-OP mode is active so the project PAKs are loaded only through MultiMod.

Expected detector state:

`MODE=COOP_MULTIMOD`

User command:

`1_SWITCH_TO_COOP_MULTIMOD.cmd`

Switcher requires both loader indicators before entering CO-OP mode:

- `ph_ft\MultiMod`
- `ph_ft\work\bin\x64\CustomPak.ini`

If these are not detected, switch must stop safely.

## Switcher commands

`0_OPEN_MULTIMOD_DOWNLOAD_PAGE.cmd`

- opens the external Data Pak Limit Bypass / MultiMod page;
- no third-party binary is bundled by THE BEAST PROJECT.

`1_SWITCH_TO_COOP_MULTIMOD.cmd`

- detect game;
- verify loader;
- verify known PAK hashes;
- build recipe `data3` from official archives;
- backup saves;
- snapshot source2/source3/multi2/multi3;
- install project `data2/data3` into MultiMod;
- verify;
- remove project copies from source;
- verify final CO-OP state.

`2_SWITCH_BACK_NORMAL_PROVEN.cmd`

- detect game;
- rebuild recipe `data3`;
- install project `data2/data3` back into source;
- verify;
- remove project copies from MultiMod;
- verify final NORMAL state.

`3_CHECK_CURRENT_MODE.cmd`

Expected status categories:

- `NORMAL_SOURCE`
- `COOP_MULTIMOD`
- `OUR_MOD_DISABLED`
- `MIXED_BOTH_LOCATIONS`
- `PARTIAL / LEGACY / UNKNOWN`

`4_DISABLE_OUR_MOD.cmd`

- removes project PAKs from both source and MultiMod;
- does **not** remove the external MultiMod/Data Pak Limit Bypass loader.

## Switcher safety

Each switch:

- requires game closed;
- creates save backup;
- snapshots source2/source3/MultiMod2/MultiMod3;
- stops on unknown PAKs;
- attempts rollback after mutation failure;
- rebuilds recipe `data3` from current official `data0/data1`.

## Proven CO-OP runtime result

**Major milestone:** user enabled `COOP_MULTIMOD` and successfully joined sibling's world while sibling remained vanilla and did not install the gameplay mod.

Therefore this exact scenario is **RUNTIME PROVEN**:

USER:

- Data Pak Limit Bypass / MultiMod;
- USER HIGH LOOT SPECIAL45 gameplay payload in MultiMod.

SIBLING:

- vanilla gameplay;
- no THE BEAST PROJECT gameplay mod.

RESULT:

- user successfully joined sibling's vanilla world.

Freeze the NORMAL <-> CO-OP switch mechanism unless a concrete runtime failure requires a change. Future gameplay patches should ideally replace only the known `data2` payload and extend the switcher's known-hash list.

---

# POC-001 — Native Legendary Opportunity/Camp Axe — FROZEN GREEN

Local-only artifact SHA-256:

`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

Confirmed runtime result:

- Camp Axe generated as **Legendary One-Handed Axe** from a vanilla Rare-path definition.
- Legendary identity, affixes, damage `131`, durability `160/160`, and repairs `7/7` survived save/reload and POC removal.
- Definition-added Tip/Shaft/Grip sockets did **not** survive uninstall; only vanilla Charm Socket remained.

Frozen conclusion: rarity/affixes/damage/durability/repair count can persist per item strongly enough to survive mod removal; definition-only socket structure cannot be used as persistent Ascension state.

# POC-002 — Persistent native installed-mod probe — FROZEN GREEN

Rejected delivery iterations:

- Initial custom Biter loot subroutine removed corpse `F` interaction.
- POC-002B patched wrong resource subroutine due ambiguous global anchor.
- POC-002C correctly patched `Biter_CommonResources`, but outer vanilla RNG produced too many `Nothing` outcomes.
- POC-002D forced the resource path and removed `Nothing`, but Shock T4 still did not materialize as loose CraftPart.
- POC-002E StartupMod path remains a valid fallback but was not needed for the successful persistence proof.

Successful manual Venom persistence test on the Legendary Camp Axe:

**Before Venom:**

- damage `131`
- durability `160/160`
- repairs `7/7`
- Legendary rarity and three rolled affixes
- Tip/Shaft/Grip/Charm exposed and empty

**After native Venom installed into Tip:**

- visible `Venom — Applies TOXIC on critical hits`
- damage `137` (`+6`)
- durability `185/185` (`+25`)
- repairs `7/7`
- rarity and rolled affixes unchanged

**Save -> quit -> reload with POC present:** PASS.

**After POC uninstall and vanilla reload:** PASS.

- damage remained `137`
- durability remained `185/185`
- repairs remained `7/7`
- Legendary rarity and rolled affixes remained
- Tip/Shaft/Grip UI disappeared; only Charm remained
- Venom hardware/green visual remained attached
- Toxic combat proc remained functional after uninstall

Frozen conclusion: native installed per-item mod/effect state, stat changes, visual attachment, and functional effect can serialize strongly enough to survive removal of the POC that exposed the socket. This remains useful, but POC-003 proved that arbitrary replacement of the carrier's definition-level stat magnitude is not itself serialized per item.

# POC-003 — Legendary -> L+1 persistent carrier probe — RUNTIME COMPLETE / CUSTOM STAT SIGNATURE FAILED UNINSTALL

Project-authored builder:

`tools/build_poc003_l1_carrier.py`

Detailed contract:

`patches/poc/POC_003_L1_CARRIER.md`

Runtime record:

`tests/results/POC_003_RUNTIME_UNINSTALL_RESULT.md`

Local-only `data2.pak` SHA-256:

`5608ecb1336ca84c80bc1472000ab9b50eb79a94a8a6a6c1b127f370cd31e17a`

Local user-test package SHA-256:

`a1eee27144a7ac612d0600bce57fa117d3ea8a915ca8ca258ae1615b13655a59`

POC design:

- generate a new Legendary Camp Axe through the controlled POC-001 acquisition path;
- attach native `ShockMod_Random_FT_T4_TIP` via `StartupMod(...)`;
- temporarily give that carrier a deliberately non-vanilla signature:
  - `CraftingEffect_IncreasedDamageMul` level `8`;
  - `CraftingEffect_IncreasedDurability` level `3` (`+18%`);
  - attack speed unchanged.

Runtime result:

**Initial / POC active:**

- damage `147`
- durability `160/188`
- repairs `7/7`
- visible affixes: `+6% Damage (Infected)`, `+20% Damage (Accessories)`, `-7.5% Stamina Cost (Melee Weapons)`
- `Spark — Applies SHOCK on critical hits` visible

**Save -> quit -> reload with POC-003 installed:** PASS.

- damage remained `147`
- durability remained `160/188`
- repairs remained `7/7`
- affixes and Spark remained visible

**After POC-003 uninstall -> vanilla reload:**

- Legendary rarity preserved
- listed affixes preserved
- damage changed `147 -> 142`
- max durability changed `188 -> 185`
- current durability remained `160`
- repairs remained `7/7`
- POC-added Tip/Shaft/Grip UI disappeared; only Charm Socket remained
- Spark UI disappeared with the definition-added socket exposure
- Shock hardware/visual attachment still appeared physically attached in the supplied screenshot
- post-uninstall SHOCK proc functionality was not directly combat-tested for this exact POC-003 item

Frozen interpretation:

- **Strong persistence pass rejected.** The exact POC-003 custom stat values did not survive POC removal.
- Current durability remaining `160` while max durability recomputed `188 -> 185` is consistent with current item condition being serialized separately from the carrier's definition-resolved max-stat contribution.
- A native installed-mod identity/attachment may persist, but arbitrary custom modifier magnitude supplied by a temporary CraftPart definition is not proven serialized per item.
- Do **not** extend this parameter-override strategy to L+2..L+5.
- Next Ascension research must identify a different serialized per-item field/state or a native carrier whose magnitude itself is stored on the item instance.

---

# Manual Save Anywhere research — PAUSED / CLOSED TEMPORARILY

User decision on 2026-09-22: **stop Manual Save Anywhere work for now. Do not continue collectors, native hooks, position-restoration experiments, or extra user test cycles unless the user explicitly reopens this feature.**

## What was actually proven

- DebugConf/ConsoleCommand was tested through packed, loose, EXE-adjacent, and explicit `-debugconf=` routes; visible `HideHUD()` canaries never executed. This route is a frozen dead end for retail 1.71E.
- Native binary mapping V7-V11 recovered real save-system structures and call paths in `gamedll_ph_x64_rwdi.dll`, including `SaveController`, `SaveRequestController`, their vtables, the native save dispatcher, quick-save selector behavior, and the game's own caller setup.
- Runtime helper refinements through POC-J/J2/J3/J4 fixed status output, PowerShell `$PID` collision, and process discovery.
- POC-J4 successfully found and validated exactly one active `SaveController` object, backed up the test save, armed the controller on F5, and observed the real Steam save file change immediately afterward.
- The successful F5 sequence showed native controller state transition from inactive to armed and then back to inactive after the engine processed it; the watched `save_ft_0.sav` changed in the same trigger window.

## What remains unresolved

- The F5-native trigger is a **real save-file-write proof**, but it is **not** accepted as a complete Save Anywhere feature.
- Inventory/progression persistence is insufficient proof because vanilla saves those normally.
- Exact last-player-position restoration was not established to the user's satisfaction.
- A possible future implementation could pair native save with explicit position/rotation/map capture and post-load restoration, but the user chose not to pursue that now.

## Frozen conclusion

Manual Save Anywhere is **not GREEN**, **not deleted**, and **not an active workstream**. Preserve all findings for a possible future reopen, but spend zero further development/test effort on it until explicitly requested.

---

# Historical failures / rejected builds

Do not recommend or reuse these as active builds:

## A3/DLC failure lineage

- `DLTB_A1_A2_A3_V3.zip` — produced `DLC ITEMS DISABLED` popup.
- `DLTB_A1_A2_A3_V31_SAFE.zip` — also failed.
- `DLTB_EMERGENCY_RECOVER_PRE_V3.zip` — recovery attempt did not solve that lineage.

A3 remains suspended.

## Aggressive V3 FINAL LootedObject rewrite

Runtime failure:

- corpse `F` prompt disappeared.

Frozen conclusion:

- never repeat the aggressive `LootedObject` rewrite.

## Old STEP1 runtime-merge installer

`DLTB_V3_GREEN_VANILLA_RECIPE_OUTPUT_STEP1.zip`

Do not reuse.

Observed failure state included missing `data2.pak`, so game ran vanilla. This did not prove recipe content itself was invalid; it proved that installer architecture/state handling was unsafe.

## STEP1 FIXED V2

Failed with:

`Argument types do not match`

Abandoned.

## STEP1 V3

False duplicate Steam-library detection caused safe-stop / non-install behavior.

Abandoned.

## STEP1 V4

Succeeded and proved the safer architectural split:

- `data2` = gameplay/loot;
- `data3` = output-only recipe override.

That architecture was carried forward into current one-click packages.

---

# Total clean / emergency recovery tool

Local artifact:

`DLTB_TOTAL_CLEAN_TOOL.zip`

SHA-256:

`1b1e638217a8e8051ce6f981274eaea2dac2d0a0defc7a558eafade327e73de9`

Purpose: local DLTB cleanup/reset when needed.

Can target local game/install leftovers such as game folder, Steam userdata AppID `3008130`, Documents, shader/downloading/compatdata, and manifest-related local state.

Steam Cloud server data is **not** directly deleted by the script.

Official Steam save location used by project tooling:

`Steam\userdata\<SteamID>\3008130\remote\out\`

Use only for emergency recovery / clean reinstall, not routine patching.

---

# Technical invariants

- Do not commit proprietary PAKs, vanilla extracted archives, saves, DLLs, EXEs, or local-only binary test artifacts.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists merely because it survives reload while the mod remains installed.
- Definition-only sockets remain runtime-dependent.
- Keep held-weapon drop and extra corpse-loot weapon rolls separate.
- Attack speed remains safety-sensitive.
- Scope loot-builder edits to exact named blocks; no ambiguous global first-match anchors.
- For Windows helper packages: user launches `.cmd`; `.cmd` launches `.ps1`, status/log output is explicit, and CMD stays open with `pause` on both success and failure.
- Distinguish **FILESYSTEM_INSTALL** from **ENGINE_LOAD / runtime effect** in every future installer/test.
- Treat current corpse routing, `data2/data3` split, and NORMAL<->COOP switcher as frozen-green structures.
- Future gameplay patches should ideally change only the known `data2` payload and extend known-hash detection.

# Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** NOT persistent.
- **POC-002 native installed-mod stat persistence:** GREEN for tested Venom-on-Camp-Axe path.
- **Installed Venom visual attachment after uninstall:** GREEN.
- **Functional Toxic proc after uninstall:** GREEN.
- **POC-003 with-POC save/reload:** PASS.
- **POC-003 arbitrary custom L+1 stat signature after uninstall:** NOT persistent / NOT GREEN.
- **CORPSE SAFE A1+A2 routing:** GREEN.
- **GREEN `data2` + separate recipe `data3` architecture:** GREEN.
- **Current one-click `data2/data3` install architecture:** proven enough for active use.
- **COOP_MULTIMOD -> join vanilla sibling world:** RUNTIME GREEN for the tested setup.
- **Manual Save Anywhere:** PAUSED / NOT GREEN. Native F5 save-file write is proven; exact position behavior unresolved.

# Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine.
2. POC-002B ambiguous global anchor.
3. POC-002C inner-weight-only test delivery.
4. POC-002D loose CraftPart through Biter resources.
5. POC-003 temporary native CraftPart parameter override as an arbitrary uninstall-persistent Ascension magnitude carrier.
6. Manual Save POC-A direct `_ACTION_QUICK_SAVE` binding.
7. `debugconfdefault.scr` override from inside `data2.pak`.
8. physical `ph_ft\source\debugconfdefault.scr` as a reliable retail DebugConf load path.
9. physical EXE-adjacent `debugconfdefault.scr` as a reliable retail DebugConf load path.
10. explicit `debugconf.scr` + `-debugconf=` as a reliable retail runtime route.
11. Aggressive `LootedObject` rewrite that removed corpse `F` interaction.
12. A3 inventory/player-variable lineage that triggered DLC-disable behavior.
13. Old STEP1 merge-in-place architecture that could leave `data2` absent.

POC-B/C/D/E remain **inconclusive command probes**, not proof that the underlying native save functions themselves fail.

---

# Current canonical local artifacts

These are local/user artifacts and are **not committed** to the repository.

## Main user gameplay

`DLTB_ONECLICK_USER_HIGH_LOOT_SPECIAL45.zip`

`data2` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Package SHA-256:

`780ce15ce103febee1f9ebd3d35a272c3635e8683f07f404b4f9094b9890429c`

## NORMAL / CO-OP switcher

`DLTB_USER_SPECIAL45_MODE_SWITCHER.zip`

Package SHA-256:

`55f20cdc44dda8ad9c79d0d1671bf302ee7a0b1410adbb9bba36bb02d5ed28e7`

Embedded gameplay `data2` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Runtime milestone:

**CO-OP with vanilla sibling = PROVEN SUCCESS.**

## Optional sibling balanced build

`DLTB_ONECLICK_SIBLING_BALANCED_SPECIAL45.zip`

`data2` SHA-256:

`ab18b545bffbee00ff8ff8ee1e0a9b241bfb2f5864aa88bedc282dab428e771d`

Package SHA-256:

`4e7013a60c10acadaa98a04af78205333cfc86796572227d99d78ebc3c5311b6`

Sibling currently chooses vanilla instead.

---

# next_safe_action

When development resumes:

1. Treat **USER HIGH LOOT SPECIAL45** as the canonical user gameplay baseline.
2. Preserve corpse routing / `LootedObject` topology.
3. Preserve the `data2` gameplay + `data3` recipe split.
4. Preserve the NORMAL <-> COOP MultiMod switch mechanism.
5. Preserve current resource **chance** and `33++` / Scrap `40++` **quantity** behavior unless the user explicitly asks for rebalance.
6. Preserve the six-ammo-blueprint one-bundle behavior.
7. Preserve Special Infected Legendary `45%` semantics as **share inside the existing project weapon rarity route**, not an absolute per-kill chance.
8. Viral stays excluded from Special45 unless explicitly requested.
9. Do not reintroduce A3, `player_variables`, stash/versioning changes, or aggressive corpse rewrites.
10. Prefer the next gameplay patch as numeric/sub-pool changes in `data2` only.
11. Extend installer/switcher known-hash detection for any new canonical `data2` payload.
12. Test NORMAL mode first after each gameplay payload change:
    - modified-data behavior as expected;
    - no `DLC ITEMS DISABLED`;
    - corpse `F` works;
    - loot/resources behave as intended;
    - recipe `data3` still works;
    - save/reload stable.
13. Then test `COOP_MULTIMOD` and confirm joining sibling's vanilla world still works.
14. Keep POC-001 and POC-002 frozen green.
15. Keep Manual Save Anywhere paused unless explicitly reopened.
16. Keep POC-003 custom magnitude strategy rejected; do not build L+2..L+5 from it.
17. Deeper Ascension research may resume only by finding a genuinely per-item serialized state/carrier whose magnitude survives definition removal.
