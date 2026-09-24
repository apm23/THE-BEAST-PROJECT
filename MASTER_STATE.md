# MASTER_STATE

## Authority

This file plus actual GitHub `main` HEAD are authoritative for continuation. Reconcile both before acting.

Continuity phrase:

`BEAST-PROVEN-SWITCH45`

Interpret it as: continue THE BEAST PROJECT from this exact state, preserve proven runtime structures, use the committed portable baseline/rebuild tooling, and do not restart rejected experiments.

---

# Baseline / repository identity

- Repository: `apm23/THE-BEAST-PROJECT`
- Game: **Dying Light: The Beast**
- Target build: **VER. 1.71E**
- Steam AppID: **3008130**
- Clean archive map captured from the original development machine: `data0.pak,data1.pak`.
- Clean save remains local/private and must never be committed.
- Repository is **source/tooling/config/audit only**.
- Never commit proprietary game PAKs, raw extracted vanilla files, saves, DLLs, EXEs, third-party loader binaries, or built local gameplay packages.

## Original 1.71E baseline capture

The original project session captured:

- `AllPathCount=19727`
- `RelevantPathCount=366`
- targeted vanilla extraction: **58 requested files**
- targeted extraction result: **58 extracted / 0 missing**
- original capture timestamp: `2026-09-20T17:19:02.1011483+09:00`

Original local proprietary reference ZIP:

`DLTB_TARGETS_1.71E.zip`

SHA-256:

`09a57b50bffd90f9862b36377384b172e23770787ab086b2a65809a9d63455bb`

That ZIP and its 58 raw vanilla files are intentionally **NOT** in Git. They are reproducible from an owned 1.71E install using the committed extractor + exact hash manifest.

Committed baseline contract:

- `config/baseline_1.71E_capture.json`
- `config/baseline_1.71E_targets.txt`
- `config/baseline_1.71E_manifest.json`
- `tools/extract_targeted_baseline_1.71E.ps1`

`baseline_1.71E_manifest.json` contains exact path, source archive, byte size, and SHA-256 for all 58 captured files.

The exact 366 project-relevant archive-path metadata records are stored in:

`config/relevant_file_list_1.71E/part01.txt` through `part06.txt`

Concatenate those six files in lexical order to reconstruct the original 366-line relevant path list. They are metadata only, not vanilla file contents.

---

# PORTABLE EXECUTION CONTRACT — CURRENT / IMPORTANT

The project is now designed so the current proven user gameplay payload can be reconstructed on a fresh Windows machine without carrying the old chat or local binary package.

## Fast bootstrap

Requirements:

1. Clone this repository.
2. Have an owned/local Dying Light: The Beast installation matching **1.71E**.
3. Python 3 installed.
4. 7-Zip recommended; `tar.exe` is a fallback for extraction if it can read the PAK.

Run:

`tools\BOOTSTRAP_1.71E_USER_SPECIAL45.cmd`

Bootstrap source:

- `tools/BOOTSTRAP_1.71E_USER_SPECIAL45.cmd`
- `tools/bootstrap_1.71E_user_special45.ps1`

Bootstrap performs:

1. locate the Steam DLTB install;
2. extract the exact 58-file local baseline;
3. validate all 58 files against captured 1.71E SHA-256 + byte size;
4. rebuild the canonical USER HIGH LOOT SPECIAL45 `data2_payload.pak` from compact project-authored delta patches;
5. require the exact canonical final PAK hash;
6. copy the verified payload to `tools/runtime_switcher/data2_payload.pak` so the proven NORMAL/CO-OP switcher source is ready.

Local baseline output:

`local_baseline/1.71E/`

Local build output:

`local_build/USER_HIGH_LOOT_SPECIAL45/data2_payload.pak`

Both are gitignored.

## Exact canonical payload rebuild

Builder:

`tools/build_user_special45_payload.py`

Patch source:

`patches/runtime/USER_HIGH_LOOT_SPECIAL45_1.71E/`

The patch directory stores compressed/base64 project delta instructions, not full vanilla definitions.

Only three verified baseline definitions are needed for the canonical final `data2`:

### `scripts/inventory/inventory_ranged.scr`

Captured 1.71E baseline SHA-256:

`610622dae7450d36a873ea630dbf9fac2757e359fa4d159b23305a0590b82b20`

Canonical final patched file SHA-256:

`8bf5e4d097972ed9075f6105efe4e5fb533d44ecd5f3dd39cc44fb5bd210f745`

### `scripts/inventory/loot/lootpools_ft.loot`

Captured 1.71E baseline SHA-256:

`fac968e396e185888f20cdfc20543f4a492d10f21f5dde0c8f8b2c9c054a9f98`

Canonical final patched file SHA-256:

`46fe4e2c3c63e68fda99c80c1982689cbd874f16c1c173e2fa6643501be8635e`

### `scripts/inventory/loot/lootsets_ft.loot`

Captured 1.71E baseline SHA-256:

`9addc1fbfb35b56c8be9928307208b12f3f0672cf303affdba661a4193d6410a`

Canonical final patched file SHA-256:

`b6f2f78ab4a2c0dcf1a1feddd2129de4c60eedb4900c894e628c91292669c308`

Canonical final `data2_payload.pak` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

The deterministic builder was tested locally against the original canonical USER HIGH LOOT SPECIAL45 PAK and produced **byte-for-byte identical output**.

Manual rebuild after baseline extraction:

`python .\tools\build_user_special45_payload.py --prepare-switcher`

Portable/reproduction documentation:

`docs/PORTABLE_REPRODUCTION.md`

Artifact/hash history:

`docs/ARTIFACT_INDEX.md`

### Portability rule

Do not make the repo "portable" by uploading raw vanilla extraction. Portability is achieved by:

**exact baseline fingerprint + local extraction + project delta patch + deterministic rebuild tooling.**

---

# Current phase

**CURRENT RUNTIME-GREEN PLAY STATE:** the project has moved past the failed A1+A2+A3 V3 lineage. The current proven architecture is:

- A1+A2 gameplay/loot in `data2.pak`;
- vanilla special-ammo output-only overrides in separate `data3.pak`;
- one-click/detected install architecture;
- proven NORMAL <-> CO-OP MultiMod switch architecture.

Current canonical user gameplay profile:

**USER HIGH LOOT SPECIAL45**

Important status:

- corpse `F` interaction: **runtime GREEN** on frozen corpse-safe lineage;
- DLC behavior: **runtime GREEN** on current lineage;
- `data2` / `data3` split: **runtime GREEN**;
- recipe output-only `data3`: proven working;
- NORMAL <-> COOP switcher: **runtime proven**;
- modded user successfully joined sibling's vanilla world in COOP_MULTIMOD;
- sibling currently chooses vanilla and does not install gameplay mod;
- A3 inventory expansion: **SUSPENDED**;
- Manual Save Anywhere: **PAUSED / NOT ACTIVE**;
- POC-001 and POC-002: frozen green;
- POC-003 arbitrary custom L+1 magnitude strategy: rejected;
- final Legendary Core + true uninstall-persistent Ascension L+1..L+5: not implemented yet.

---

# Hard safety rules

Priority order:

1. Save / DLC safety.
2. Corpse loot interaction must remain functional (`F`).
3. Preserve runtime-proven structures.
4. Prefer numeric/sub-pool changes over structural rewrites.
5. Keep install, detection, rollback, and cleanup explicit.
6. Preserve working CO-OP with vanilla sibling.

Do **not** reintroduce or casually modify:

- A3 inventory expansion;
- `player_variables`;
- `stash_dlc`;
- inventory versioning;
- quickslot/stash rewrites;
- save-versioning paths;
- DLC-sensitive files;
- aggressive `LootedObject` structure replacement;
- delete/reorder/add corpse branches without separate proof;
- `VisibleQuickSlotsCount` / invented SLOT5-SLOT8 behavior.

Historical hard failure: an aggressive rewrite of `scripts/inventory/loot/lootpools_ft.loot` caused corpse loot prompt `F` to disappear.

Therefore:

**`LootedObject` topology / corpse routing is FROZEN.**

Preferred future gameplay changes:

- numeric weights;
- existing sub-pool contents;
- min/max quantities;
- safe isolated definitions already following proven structure.

---

# Frozen project goals

1. Universal native Legendary eligibility even for weapons vanilla-capped at Rare/Epic.
2. Per-weapon rarity gacha while preserving RNG/farming.
3. Increased but controllable weapon availability from infected/humans/supported loot sources.
4. Keep human held-weapon behavior separate from extra corpse-loot weapon rolls.
5. Legendary must be real native item quality/state, never cosmetic text/color only.
6. Legendary Core: Rare/Epic -> Legendary; Legendary -> per-item Ascension.
7. Ascension target: L -> L+1 -> L+2 -> L+3 -> L+4 -> L+5.
8. Ascension emphasizes damage/durability; secondary stats moderate; attack speed conservative.
9. Prefer genuinely serialized per-item progression over global definition-only buffs.
10. Preserve weapon identity/model/class.
11. Keep RNG/farming in final design.
12. Manual Save Anywhere remains a future idea but stays paused until explicitly reopened.

---

# Confirmed 1.71E mapping

See:

`docs/BASELINE_1.71E_MAPPING.md`

Key conclusions:

- Blue = Rare; Violet = Epic; Orange = Legendary; Platinum/Exotic exist above Orange.
- Native Legendary generation uses class-specific Legendary affix groups plus `Weapons_Random_Legendary_ft`.
- Lower-rarity definitions can hardcode Rare affix groups; Universal Legendary cannot be cosmetic-only.
- Inspected human weapon presets use held-weapon `LootChance(1.0)` where present.
- `StartupMod(...)` is a confirmed native generation mechanism.
- Loose `CategoryType_CraftPart` delivery through ordinary Biter resource loot is rejected as a test-delivery route after runtime failure.

---

# Current proven gameplay lineage

## CORPSE SAFE A1+A2 — structural runtime-GREEN ancestor

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

Preserve its corpse-routing topology.

## GREEN BALANCED — safe lower-loot reference

Local artifact:

`DLTB_V3_GREEN_BALANCED.zip`

Package SHA-256:

`a7f02823958e09b2d2b2111a81870fc98ea2ae37adeccc37338b47c0dce35ced`

`data2.pak` SHA-256:

`ecbbbc1ca3725c4507ce6e3f893c5e3438dc882e1a4bd4b69dbff4457812609e`

This was built strictly from the runtime-GREEN corpse-safe base and became the low-loot/reference balance ancestor.

---

# A1 — custom standard firearm ammo

Six project-authored standard firearm recipes:

- Pistol: `10 Scrap -> 60`
- Revolver: `14 Scrap -> 24`
- SMG: `18 Scrap -> 120`
- Shotgun: `24 Scrap -> 24`
- Rifle: `30 Scrap -> 80`
- Marksman: `37 Scrap -> 32`

## Six-blueprint bundle

All six custom ammo craftplans are delivered by one bundle item:

`DLTB_PlayNow_AllAmmoBlueprints`

Bundle contents:

- `Craftplan_PlayNow_Ammo_Pistol`
- `Craftplan_PlayNow_Ammo_SMG`
- `Craftplan_PlayNow_Ammo_Rifle`
- `Craftplan_PlayNow_Ammo_Shotgun`
- `Craftplan_PlayNow_Ammo_Revolver`
- `Craftplan_PlayNow_Ammo_Marksman`

**One bundle drop = all six custom ammo craftplans.**

Do not split them back into six independent blueprint drops unless explicitly requested.

---

# Vanilla special-ammo recipe patch — proven `data3`

Final architecture:

- `data2.pak` = gameplay / loot / A1+A2;
- `data3.pak` = vanilla recipe output-only overrides.

`data3` is generated from the user's current official `data0.pak` / `data1.pak`, not from redistributed vanilla source.

Current output quantities:

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

**RequiredItem ingredients stay vanilla.**

Relevant craftplans:

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

Proven recipe source path:

`scripts/inventory/collectables_ft.scr`

Runtime recipe builder source is preserved in:

`tools/runtime_switcher/TBP_COMMON.ps1`

---

# Final resource balance

Important correction from earlier typo:

**Resource chance / route weight is NOT +40%.**

Final rule:

- keep resource chance at proven balance;
- increase quantity when a resource route is selected;
- preserve internal material relative weights;
- Scrap remains `40++` style quantity.

Typical Scrap ranges from proven lineage:

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

Existing `Craft_*` pool items include materials such as Rags, Wiring, Container, Resin, Blades, Weights, Feathers, Leather, Battery, Cleaning Supplies, Oxidizer, Alcohol, Fuel Can, etc.

Do not convert this into an independent +40% resource-chance system.

---

# Two gameplay profiles

## SIBLING BALANCED

Purpose: conservative weapon pressure.

- firearm + melee project weights: approximately GREEN x1.05;
- weapon-mod blueprint weights: approximately GREEN x1.05;
- native Legendary pressure conservative relative to old SAFE;
- resource chance remains proven baseline;
- resource quantity uses `33++` / Scrap `40++` system;
- Special45 rule applies.

Canonical local artifact:

`DLTB_ONECLICK_SIBLING_BALANCED_SPECIAL45.zip`

`data2.pak` SHA-256:

`ab18b545bffbee00ff8ff8ee1e0a9b241bfb2f5864aa88bedc282dab428e771d`

Package SHA-256:

`4e7013a60c10acadaa98a04af78205333cfc86796572227d99d78ebc3c5311b6`

Sibling ultimately declined installing gameplay mod; keep this as optional only.

## USER HIGH LOOT — current canonical profile

Purpose: weapon availability close to old A1+A2 SAFE while retaining safe final architecture.

- firearm + melee project weights ~= **97% of old A1+A2 SAFE values**;
- native firearm Legendary preference target = `3.88` versus old SAFE `4.0`;
- weapon-mod blueprint pressure remains modest ~= GREEN x1.05;
- resource chance = proven baseline;
- resource quantity = current `33++` / Scrap `40++` system;
- Special45 rule applies.

Canonical local artifact:

`DLTB_ONECLICK_USER_HIGH_LOOT_SPECIAL45.zip`

Canonical `data2.pak` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Package SHA-256:

`780ce15ce103febee1f9ebd3d35a272c3635e8683f07f404b4f9094b9890429c`

This is the payload rebuilt by the new portable tooling and used by the current NORMAL/CO-OP switcher.

---

# Special Infected Legendary 45%

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

Rule:

When the existing project weapon rarity route is selected for one of those Special Infected, **Legendary rarity share = 45%**.

More precisely:

- Firearm Legendary + Melee Legendary combined = `45%` of existing project-weapon rarity weight;
- Common/Rare/Epic share remaining `55%` preserving prior relative ratio;
- total project-weapon route weight is preserved;
- overall weapon frequency is not increased by this rule;
- resource chance is unchanged;
- no new corpse branch is added;
- NORMAL and PERMA routes are both tuned.

Important:

**This is NOT an absolute 45% Legendary chance per kill.** It is 45% share inside the existing project weapon rarity selection when that route actually hits.

---

# One-click / runtime architecture

Install philosophy:

`DETECT -> verify known hashes -> backup save -> build recipe data3 from official data0/data1 -> install data2 -> install data3 -> verify -> show status`

Unknown `data2` / `data3`:

**STOP SAFE.**

Uninstall philosophy:

`DETECT -> verify exact known project hashes/state -> remove project data2 + data3 -> verify CLEAN`

Project-authored runtime switcher source is committed under:

`tools/runtime_switcher/`

Key source files:

- `TBP_COMMON.ps1`
- `MODE_SWITCH_COMMON.ps1`
- `SWITCH_TO_COOP.ps1`
- `SWITCH_BACK_NORMAL.ps1`
- `CHECK_MODE.ps1`
- `DISABLE_OUR_MOD.ps1`
- launcher CMD files
- `STATIC_AUDIT.json`

The gameplay `data2_payload.pak` is not committed. Bootstrap regenerates the exact canonical payload locally.

---

# CO-OP / MultiMod — RUNTIME PROVEN

External compatibility layer:

Data Pak Limit Bypass / MultiMod.

Third-party loader binary is never committed or bundled by this repo.

## NORMAL / PROVEN mode

Project files:

- `ph_ft\source\data2.pak`
- `ph_ft\source\data3.pak`

Expected mode:

`NORMAL_SOURCE`

Launcher:

`tools\runtime_switcher\2_SWITCH_BACK_NORMAL_PROVEN.cmd`

## CO-OP / MULTIMOD mode

Project files:

- `ph_ft\MultiMod\data2.pak`
- `ph_ft\MultiMod\data3.pak`

Project copies at `ph_ft\source\data2.pak` / `data3.pak` are absent while CO-OP mode is active.

Expected mode:

`COOP_MULTIMOD`

Launcher:

`tools\runtime_switcher\1_SWITCH_TO_COOP_MULTIMOD.cmd`

Loader detection requires:

- `ph_ft\MultiMod`
- `ph_ft\work\bin\x64\CustomPak.ini`

Other launchers:

- `3_CHECK_CURRENT_MODE.cmd`
- `4_DISABLE_OUR_MOD.cmd`
- `0_OPEN_MULTIMOD_DOWNLOAD_PAGE.cmd`

Each switch:

- requires game closed;
- verifies known PAKs;
- rebuilds recipe `data3` from current official archives;
- backs up saves;
- snapshots source2/source3/MultiMod2/MultiMod3;
- attempts rollback after mutation failure;
- never deletes an unknown PAK.

## Proven runtime result

**Major milestone:** user enabled `COOP_MULTIMOD` and successfully joined sibling's world while sibling remained vanilla and did not install THE BEAST PROJECT gameplay mod.

Therefore this exact setup is runtime-proven:

USER:

- Data Pak Limit Bypass / MultiMod installed;
- USER HIGH LOOT SPECIAL45 payload loaded through MultiMod.

SIBLING:

- vanilla gameplay;
- no project gameplay mod.

RESULT:

- successful join to sibling's vanilla world.

Freeze NORMAL <-> CO-OP switch logic unless a concrete runtime failure requires a change.

Original switcher local ZIP:

`DLTB_USER_SPECIAL45_MODE_SWITCHER.zip`

ZIP SHA-256:

`55f20cdc44dda8ad9c79d0d1671bf302ee7a0b1410adbb9bba36bb02d5ed28e7`

---

# POC-001 — Native Legendary Opportunity/Camp Axe — FROZEN GREEN

Local-only artifact SHA-256:

`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

Runtime proof:

- Camp Axe generated as real **Legendary One-Handed Axe** from a vanilla Rare-path definition;
- Legendary identity, affixes, damage `131`, durability `160/160`, repairs `7/7` survived save/reload and POC removal;
- definition-added Tip/Shaft/Grip sockets did not survive uninstall; only vanilla Charm socket remained.

Frozen conclusion:

rarity/affixes/damage/durability/repair state can persist per item strongly enough for the tested path; definition-only socket structure cannot serve as persistent Ascension state.

---

# POC-002 — Native installed-mod persistence — FROZEN GREEN

Rejected delivery iterations included custom Biter loot subroutine, ambiguous global anchor, inner-weight-only delivery, and loose CraftPart resource delivery.

Successful manual Venom persistence proof on Legendary Camp Axe:

Before Venom:

- damage `131`
- durability `160/160`
- repairs `7/7`

After native Venom installed into Tip:

- visible Venom / Toxic effect;
- damage `137`;
- durability `185/185`;
- repairs `7/7`;
- Legendary rarity/affixes unchanged.

Save -> reload with POC present: PASS.

After POC uninstall -> vanilla reload: PASS.

- damage remained `137`;
- durability remained `185/185`;
- repairs remained `7/7`;
- Legendary rarity and affixes remained;
- temporary Tip/Shaft/Grip UI disappeared;
- Venom hardware/green visual remained;
- Toxic combat proc remained functional.

Frozen conclusion:

native installed per-item mod identity/effect/stat/visual state can serialize and survive removal of the POC that exposed the socket.

---

# POC-003 — L+1 carrier probe — REJECTED STRONG PERSISTENCE

Builder:

`tools/build_poc003_l1_carrier.py`

Contract:

`patches/poc/POC_003_L1_CARRIER.md`

Runtime record:

`tests/results/POC_003_RUNTIME_UNINSTALL_RESULT.md`

Local `data2.pak` SHA-256:

`5608ecb1336ca84c80bc1472000ab9b50eb79a94a8a6a6c1b127f370cd31e17a`

Local test-package SHA-256:

`a1eee27144a7ac612d0600bce57fa117d3ea8a915ca8ca258ae1615b13655a59`

POC attached native Shock T4 and temporarily overrode its definition magnitude.

With POC active:

- damage `147`
- durability `160/188`
- repairs `7/7`
- Spark visible

Save/reload with POC present: PASS.

After POC uninstall:

- Legendary rarity and rolled affixes persisted;
- damage recomputed `147 -> 142`;
- max durability recomputed `188 -> 185`;
- current durability remained `160`;
- repairs remained `7/7`;
- added socket UI disappeared;
- Shock attachment still appeared physically attached.

Frozen conclusion:

**arbitrary custom modifier magnitude supplied by a temporary CraftPart definition is NOT proven serialized per item.**

Do not extend this strategy to L+2..L+5.

Future Ascension research must find a different genuinely per-item serialized field/carrier whose magnitude survives definition removal.

---

# Manual Save Anywhere — PAUSED / NOT GREEN

User decision: stop this work until explicitly reopened.

What was proven:

- retail DebugConf/ConsoleCommand canary routes did not execute and are frozen dead ends;
- native binary mapping recovered SaveController / SaveRequestController paths and dispatcher behavior;
- runtime helper POC-J4 found exactly one active SaveController;
- F5 native trigger caused real save controller transition and real `save_ft_0.sav` file write.

What remains unresolved:

- exact last-player-position restoration was not proven to user's satisfaction;
- real file write alone is not accepted as complete Save Anywhere.

Do not spend development/test cycles on this unless user explicitly reopens it.

---

# Historical failures / rejected builds

Never recommend or revive these as active install candidates:

## A3 / DLC failure lineage

- `DLTB_A1_A2_A3_V3.zip` — `DLC ITEMS DISABLED` popup.
- `DLTB_A1_A2_A3_V31_SAFE.zip` — failed.
- `DLTB_EMERGENCY_RECOVER_PRE_V3.zip` — recovery attempt failed.

A3 remains suspended.

## Aggressive LootedObject rewrite

Runtime failure:

- corpse `F` prompt disappeared.

Never repeat.

## Old STEP1 merge installer

`DLTB_V3_GREEN_VANILLA_RECIPE_OUTPUT_STEP1.zip`

Observed state included missing `data2.pak`; abandoned.

## STEP1 FIXED V2

Failed:

`Argument types do not match`

## STEP1 V3

False duplicate Steam-library detection caused safe-stop/non-install.

## STEP1 V4

Succeeded and proved the current architecture:

- `data2` gameplay;
- `data3` output-only vanilla recipe override.

This split is now frozen/proven.

---

# Total clean / emergency recovery source

Original local artifact:

`DLTB_TOTAL_CLEAN_TOOL.zip`

ZIP SHA-256:

`1b1e638217a8e8051ce6f981274eaea2dac2d0a0defc7a558eafade327e73de9`

Project-authored source is now committed under:

`tools/cleanup/`

Includes scan-only and destructive local-clean launchers plus source manifest.

Use only for emergency local reset, not routine patching.

The tool can target local game folder, Steam userdata AppID `3008130`, Documents, shader/downloading/compatdata, manifest/local leftovers.

Steam Cloud server data is not directly deleted by the script.

Project save location used by tooling:

`Steam\userdata\<SteamID>\3008130\remote\out\`

---

# Technical invariants

- Never commit raw/proprietary game contents.
- Prefer project-authored patch/config/build tooling.
- Never fake Legendary using only text/color.
- Never assume persistence because something survives reload while mod remains installed.
- Definition-only sockets remain runtime-dependent.
- Keep held-weapon drop and extra corpse-loot weapon rolls separate.
- Attack speed is safety-sensitive.
- Scope loot-builder edits to exact named blocks; no ambiguous global first-match anchors.
- Windows user-facing tooling uses `.cmd` launchers, explicit status/output, and `pause` on success/failure.
- Distinguish `FILESYSTEM_INSTALL` from `ENGINE_LOAD / runtime effect`.
- Current corpse routing is frozen.
- Current `data2/data3` split is frozen.
- Current NORMAL<->COOP switch flow is frozen.
- Future gameplay patches should ideally change only deterministic `data2` patch/build inputs and extend known-hash detection.
- Raw vanilla extraction remains local and gitignored; exact fingerprints are committed instead.

---

# Frozen-green systems

- POC-001 native Legendary identity: GREEN.
- Tested Camp Axe rarity/affixes/damage/durability/repair persistence after uninstall: GREEN.
- Definition-added extra sockets after uninstall: NOT persistent.
- POC-002 native installed Venom stat persistence: GREEN.
- Installed Venom visual attachment after uninstall: GREEN.
- Functional Toxic proc after uninstall: GREEN.
- POC-003 save/reload with POC: PASS.
- POC-003 arbitrary custom L+1 magnitude after uninstall: NOT persistent / NOT GREEN.
- CORPSE SAFE A1+A2 routing: GREEN.
- GREEN `data2` + separate recipe `data3`: GREEN.
- Current one-click/detected install architecture: active/proven.
- COOP_MULTIMOD -> join vanilla sibling world: RUNTIME GREEN for tested setup.
- Portable exact USER SPECIAL45 rebuild: **BYTE-FOR-BYTE PROVEN** against canonical data2.
- Manual Save Anywhere: PAUSED / NOT GREEN; native file-write proof only.

---

# Current canonical artifacts / hashes

Binary artifacts are local-only; use `docs/ARTIFACT_INDEX.md` for complete history.

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

Embedded gameplay payload SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

Runtime milestone:

**CO-OP with vanilla sibling = PROVEN SUCCESS.**

## Optional sibling profile

`DLTB_ONECLICK_SIBLING_BALANCED_SPECIAL45.zip`

`data2` SHA-256:

`ab18b545bffbee00ff8ff8ee1e0a9b241bfb2f5864aa88bedc282dab428e771d`

Package SHA-256:

`4e7013a60c10acadaa98a04af78205333cfc86796572227d99d78ebc3c5311b6`

Sibling currently chooses vanilla.

---

# Fresh-machine execution recipe

When this project is opened from a fresh clone / fresh chat / different machine:

1. Read `MASTER_STATE.md` completely.
2. Inspect actual GitHub HEAD before writing.
3. Read `docs/PORTABLE_REPRODUCTION.md` and `docs/ARTIFACT_INDEX.md` as needed.
4. On a Windows machine with owned DLTB 1.71E, run:
   - `tools\BOOTSTRAP_1.71E_USER_SPECIAL45.cmd`
5. Require extractor result:
   - targets 58;
   - verified 58;
   - missing 0;
   - mismatch 0.
6. Require rebuilt data2 SHA:
   - `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`
7. Bootstrap places the payload beside committed switcher source.
8. Use runtime switcher commands for NORMAL or CO-OP mode.
9. Build recipe `data3` from current official `data0/data1`; do not store stale vanilla recipe file in Git.
10. If the game build is not exact captured 1.71E, extractor hash validation must fail safe instead of silently patching a different baseline.

---

# next_safe_action

When development resumes:

1. Treat **USER HIGH LOOT SPECIAL45** as canonical gameplay baseline.
2. Treat the committed exact rebuild system as canonical source-of-truth for its `data2` payload.
3. Preserve corpse routing / `LootedObject` topology.
4. Preserve `data2` gameplay + `data3` recipe split.
5. Preserve NORMAL <-> COOP MultiMod switch logic.
6. Preserve current resource chance and `33++` / Scrap `40++` quantity behavior unless explicitly rebalanced.
7. Preserve six-ammo-blueprint one-bundle behavior.
8. Preserve Special45 semantics as share inside existing project weapon route, not absolute per-kill probability.
9. Viral stays excluded from Special45 unless explicitly requested.
10. Do not reintroduce A3, `player_variables`, stash/versioning changes, or aggressive corpse rewrites.
11. Prefer the next gameplay patch as deterministic changes to the three canonical `data2` source definitions or other isolated safe definitions only when necessary.
12. For a new canonical payload, update the portable patch/build inputs and require exact hashes.
13. Extend runtime switcher known-hash detection for any new canonical `data2`.
14. Test NORMAL mode first:
    - modified-data behavior expected;
    - no `DLC ITEMS DISABLED`;
    - corpse `F` works;
    - loot/resources intended;
    - `data3` recipes work;
    - save/reload stable.
15. Then test `COOP_MULTIMOD` and confirm user can still join sibling's vanilla world.
16. Keep POC-001 and POC-002 frozen green.
17. Keep Manual Save Anywhere paused unless explicitly reopened.
18. Keep POC-003 custom magnitude strategy rejected.
19. Deeper Ascension research may resume only after finding a genuinely per-item serialized state/carrier whose magnitude survives definition removal.
