# MASTER_STATE

## Authority

This file plus actual GitHub HEAD are authoritative for continuation. Reconcile both before acting.

## Baseline

- Game: **Dying Light: The Beast**
- Target build: **VER. 1.71E**
- Fresh-install baseline captured before mod development.
- Clean save remains local/private and must not be committed.
- Clean archive map: `data0.pak,data1.pak`.
- Targeted 1.71E extraction completed locally: **58 requested files, 0 missing**.

## Current phase

**PHASE 1F — POC-001 and POC-002 are frozen green. Manual Save Anywhere research is active in parallel and has pivoted away from DebugConf/ConsoleCommand toward direct native save-controller mapping.**

Global gacha, Legendary Core, and full Ascension are not implemented yet.

## Frozen project goals

1. Universal native Legendary eligibility even for weapons vanilla-capped at Rare/Epic.
2. Global per-weapon rarity gacha; initial Legendary target ~30% per generated weapon.
3. Slightly increased weapon availability from common infected, humans, and supported loot sources.
4. Human held weapon itself participates in rarity gacha.
5. Legendary must be real item quality/state, not cosmetic recolor.
6. Legendary Core: Rare/Epic -> Legendary, Legendary -> per-item Ascension.
7. Ascension: L -> L+1 -> L+2 -> L+3 -> L+4 -> L+5.
8. Ascension emphasizes damage/durability; secondary stats moderate; attack speed conservative.
9. Per-weapon progression, not a global definition-only buff where persistent item state is possible.
10. Preserve weapon identity/model/class.
11. Keep RNG/farming in the final mod.
12. Manual Save Anywhere: hotkey-driven native save request from ordinary gameplay locations, blocked only during unsafe transient/loading/death states.

## Initial balance targets

- Legendary per generated weapon: **30%**.
- Common Biter weapon availability: **20–25%** final target.
- Human held-weapon drop: preserve confirmed vanilla `LootChance(1.0)` where present.
- Legendary Core chances: common infected 8–10%, Viral/human ~10%, special infected 12–15%, ordinary containers 8–10%, good/locked chest 12–15%, boss/Chimera 20–30%.
- Core costs: Rare/Epic->Legendary 1; L->L+1 1; +1->+2 2; +2->+3 3; +3->+4 5; +4->+5 8.

## Confirmed 1.71E mapping

See `docs/BASELINE_1.71E_MAPPING.md`.

- Blue = Rare; Violet = Epic; Orange = Legendary; Platinum/Exotic exist above Orange.
- Native Legendary generation uses class-specific Legendary affix groups plus `Weapons_Random_Legendary_ft`.
- Lower-rarity weapons can hardcode Rare affix groups; Universal Legendary cannot be cosmetic-only.
- Standard inspected human weapon presets use held-weapon `LootChance(1.0)`.
- `StartupMod(...)` is a confirmed native generation mechanism used by vanilla generated weapons.
- Direct loose `CategoryType_CraftPart` delivery through ordinary Biter corpse-resource loot is rejected as a test-delivery path after runtime failure.

## POC-001 — Native Legendary Opportunity/Camp Axe — FROZEN GREEN

Local-only artifact SHA-256:
`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

Confirmed runtime result:

- Camp Axe generated as **Legendary One-Handed Axe** from a vanilla Rare-path definition.
- Legendary identity, affixes, damage `131`, durability `160/160`, and repairs `7/7` survived save/reload and POC removal.
- Definition-added Tip/Shaft/Grip sockets did **not** survive uninstall; only vanilla Charm Socket remained.

Frozen conclusion: rarity/affixes/damage/durability/repair count can persist per item strongly enough to survive mod removal; definition-only socket structure cannot be used as persistent Ascension state.

## POC-002 — Persistent native installed-mod probe — FROZEN GREEN

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

Frozen conclusion: native installed per-item mod/effect state, stat changes, visual attachment, and functional effect can serialize strongly enough to survive removal of the POC that exposed the socket. This is the current technical foundation for persistent Ascension carriers.

## Manual Save Anywhere research

Feature remains required, but no working native manual-save trigger has been proven yet.

### Collectors and native evidence

- Collector V2/V3 failed before extraction due PowerShell executable/path parsing.
- Collector V4 removed the 7-Zip dependency and succeeded: **350 targeted files extracted, 0 failures**.
- V4 confirmed `ConsoleCommand(s)` is documented by `DebugConf.def`; `SaveGame(...)` / `SaveGameCtrl(...)` are logging config, not save-now commands.
- Collector V5 scanned engine/game binaries for filtered save-related strings without copying binaries.
- V5 established that the save system in `gamedll_ph_x64_rwdi.dll` contains native classes/identifiers including:
  - `SaveController`
  - `SaveRequestController`
  - `SaveRequestHistory`
  - `Savegame::Session::ESaveRequestPriority`
  - `Savegame::ESessionSaveability`
  - `AcceptSaveRequests` / `RejectSaveRequests`
  - `SG_AcceptSaveRequests` / `SG_RejectSaveRequests`
  - `Savegame::Tools::ConsoleCommand::BlockSaves` / `UnblockSaves`
  - `engine.Savegame.DebugTools.Command.BlockSaveController` / `UnblockSaveController`
  - `game.Savegame.Tools.Debug.Save.ForcedAutosave`
  - `game.Savegame.Tools.Debug.Save.SaveFromQuests`
  - `game.Savegame.Tools.Debug.Save.SaveOnSessionExit`
  - `game.Savegame.Tools.Debug.FullSave.PerformFullSave`
  - `game.Savegame.Tools.Debug.FullSave.PerformFullSaveNoPreparation`
  - `_ACTION_QUICK_SAVE`
- Collector V6 searched physical files, archives, and 72 EXE/DLL binaries for DebugConf load evidence. It found:
  - `PhysicalDebugConfFiles=0` in the clean game tree;
  - archive entries `data0.pak: debugconf.def` and `debugconfdefault.scr`;
  - binary strings `debugconf.scr`, `-debugconf=`, and `-debugconf =` in the retail binaries;
  - actual game executable `ph_ft\work\bin\x64\DyingLightGame_TheBeast_x64_rwdi.exe`.

### Manual-save / DebugConf POC history

**POC-A — bind F5 to `_ACTION_QUICK_SAVE`: no observed save.**

- package installed successfully after CMD line-ending fix;
- F5 produced no watched save-file change;
- direct hidden-action binding is rejected for now.

**POC-B/C/D — save command probes through a virtual NUMPAD-SUBTRACT helper: inconclusive as save commands.**

- helper itself was proven at runtime: F6 detected, foreground title was `Dying Light: The Beast`, virtual NUMPAD SUBTRACT sent;
- no watched `.sav` change for ForcedAutosave / PerformFullSave / PerformFullSaveNoPreparation;
- later DebugConf load tests showed these commands may never have been executed, so do not freeze them as native save-function failures.

**POC-E — TeleportPlayerToRestingPlace ConsoleCommand canary: no teleport.**

- also inconclusive until DebugConf loading was validated.

**POC-F — `debugconfdefault.scr` inside `data2.pak` + `HideHUD()`: FAIL TO LOAD.**

- installed and uninstalled screenshots both retained normal HUD.
- Root DebugConf cannot be assumed overrideable through the ordinary `data2.pak` mod path.

**POC-G — physical `ph_ft\source\debugconfdefault.scr`: HUD remained normal.**

- no runtime evidence that this loose source path is consumed by the retail engine.
- earlier installer UX was insufficiently explicit, so later packages added filesystem verification/status files.

**POC-H — verified physical file beside game EXE as `debugconfdefault.scr`: FILESYSTEM PASS / ENGINE CANARY FAIL.**

- installer explicitly verified target path, marker, `HideHUD()`, size, and SHA-256 and kept CMD open;
- runtime screenshot still showed full HUD;
- therefore a correctly installed `debugconfdefault.scr` beside the EXE was not enough to make the retail engine execute `HideHUD()`.

**POC-I — V6-driven explicit `debugconf.scr` + `-debugconf=` launch: FILESYSTEM + LAUNCH REQUEST PASS / HUD CANARY FAIL.**

- V6 found exact retail strings `debugconf.scr` and `-debugconf=`;
- installer verified `ph_ft\work\bin\x64\debugconf.scr` with marker and `HideHUD()`;
- launcher requested Steam AppID `3008130` with explicit `-debugconf=<absolute path>`;
- user confirmed steps 1–7 completed as instructed;
- resulting gameplay screenshot still showed the normal HUD (quest text, safe-zone/compass strip, health/stamina, item bar, world markers).

### DebugConf conclusion — FROZEN DEAD END FOR THIS PROJECT

The DebugConf/ConsoleCommand route is no longer a productive basis for Manual Save Anywhere on retail build 1.71E. Even after verified filesystem placement and an explicit `-debugconf=` launch request, the visible `HideHUD()` canary did not execute. Whether Steam strips/rewrites the argument or the retail build ignores/restricts DebugConf, the route is not reliable enough for the mod.

Do not spend more user test cycles on DebugConf path guesses or ConsoleCommand save strings. Continue from direct native save-controller mapping instead.

### Current artifact / next native step

Local-only **Collector V7 — Native Save Xref Collector** is the next safe action.

It targets only `gamedll_ph_x64_rwdi.dll` and exports no game binary. It maps:

- exact RVAs for save-controller strings/classes;
- RIP-relative code xrefs in `.text`;
- containing function boundaries from `.pdata`;
- other ASCII strings referenced by those functions;
- limited hex windows around relevant xrefs;
- data/RVA references and PDB/debug-path strings.

Primary targets include `SaveRequestController`, `SaveController`, `AcceptSaveRequests`, `RejectSaveRequests`, `ESaveRequestPriority`, `ESessionSaveability`, Block/UnblockSaves, ForcedAutosave, SaveFromQuests, SaveOnSessionExit, PerformFullSave, and hidden quick-save strings.

Goal: identify exact 1.71E native function boundaries/signatures before attempting any runtime native hook or direct save request.

## Technical invariants

- Do not commit proprietary PAKs, vanilla extracted archives, saves, DLLs, EXEs, or local-only binary test artifacts.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists merely because it survives reload while the mod remains installed.
- Definition-only sockets remain runtime-dependent.
- Keep held-weapon drop and extra corpse-loot weapon rolls separate.
- Attack speed remains safety-sensitive.
- Scope loot-builder edits to exact named blocks; no ambiguous global first-match anchors.
- Test-delivery builds may be deterministic; final balance must return to frozen RNG targets.
- For Windows helper packages: user launches `.cmd`; `.cmd` launches the `.ps1`, status/log output is explicit, and the CMD stays open with `pause` on both success and failure.
- Distinguish **FILESYSTEM_INSTALL** from **ENGINE_LOAD / runtime effect** in every future installer/test.

## Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** NOT persistent.
- **POC-002 native installed-mod stat persistence:** GREEN for tested Venom-on-Camp-Axe path.
- **Installed Venom visual attachment after uninstall:** GREEN.
- **Functional Toxic proc after uninstall:** GREEN.

## Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine.
2. POC-002B ambiguous global anchor.
3. POC-002C inner-weight-only test delivery.
4. POC-002D loose CraftPart through Biter resources.
5. Manual Save POC-A direct `_ACTION_QUICK_SAVE` binding.
6. `debugconfdefault.scr` override from inside `data2.pak`.
7. physical `ph_ft\source\debugconfdefault.scr` as a reliable retail DebugConf load path.
8. physical EXE-adjacent `debugconfdefault.scr` as a reliable retail DebugConf load path.
9. explicit `debugconf.scr` + `-debugconf=` as a reliable retail runtime route for this mod.

POC-B/C/D/E remain **inconclusive command probes**, not proof that the underlying native save functions themselves fail.

## next_safe_action

1. Keep POC-001 and POC-002 frozen green.
2. Uninstall POC-I to leave the game tree clean.
3. Run **Collector V7 — Native Save Xref Collector** and analyze the returned 1.71E function/xref map.
4. Identify the smallest exact native call path that submits/accepts a save request through `SaveRequestController` / `SaveController` rather than DebugConf.
5. Only after exact function/signature mapping, build a disposable-test-save native hook POC with explicit install verification and a save-file watcher.
6. In parallel, continue the smallest controlled Legendary -> L+1 persistent Ascension carrier POC without perturbing frozen-green paths.
