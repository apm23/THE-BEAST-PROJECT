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

**PHASE 1F — POC-001 and POC-002 are frozen green. Manual Save Anywhere research is active in parallel.**

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

### Collectors

- Collector V2/V3 failed before extraction due PowerShell executable/path parsing.
- Collector V4 removed 7-Zip dependency and succeeded: **350 targeted files extracted, 0 failures**.
- V4 confirmed `ConsoleCommand(s)` is documented by `DebugConf.def` as running at game start or when numpad-subtract is pressed.
- V4 also confirmed `SaveGame(...)` / `SaveGameCtrl(...)` are logging config, not a save-now command.
- Collector V5 scanned engine/game binaries for filtered save-related strings without copying binaries.

Important V5 strings/classes:

- `_ACTION_QUICK_SAVE`
- `MenuSaveLoad_InfoQuickSaveOK`
- `SaveController`
- `SaveRequestController`
- `SaveRequestHistory`
- `Savegame::Session::ESaveRequestPriority`
- `AcceptSaveRequests`
- `RejectSaveRequests`
- `SG_AcceptSaveRequests`
- `SG_RejectSaveRequests`
- `engine.Savegame.DebugTools.Command.BlockSaveController`
- `engine.Savegame.DebugTools.Command.UnblockSaveController`
- `game.Savegame.Tools.Debug.Save.ForcedAutosave`
- `game.Savegame.Tools.Debug.Save.SaveFromQuests`
- `game.Savegame.Tools.Debug.Save.SaveOnSessionExit`
- `game.Savegame.Tools.Debug.FullSave.PerformFullSave`
- `game.Savegame.Tools.Debug.FullSave.PerformFullSaveNoPreparation`

### Rejected manual-save POCs

**POC-A — bind F5 to `_ACTION_QUICK_SAVE`: FAIL.**

- package installed successfully after CMD line-ending fix;
- F5 produced no observed save and no watched save-file change;
- direct hidden action binding is rejected for now.

**POC-B — `game.Savegame.Tools.Debug.Save.ForcedAutosave`: FAIL.**

- user keyboard has no numpad, so an F6 helper injected virtual NUMPAD SUBTRACT;
- helper was fixed to remove a wrong hardcoded process-name gate;
- runtime evidence showed F6 detected, foreground title `Dying Light: The Beast`, and virtual NUMPAD SUBTRACT sent repeatedly;
- no `*** CHANGED ***` event from watched `.sav` file.

**POC-C — `game.Savegame.Tools.Debug.FullSave.PerformFullSave`: FAIL.**

- F6 trigger path confirmed active against the game window;
- no watched save-file write.

**POC-D — `game.Savegame.Tools.Debug.FullSave.PerformFullSaveNoPreparation`: FAIL.**

- user reports same result as POC-C: no save-file change;
- screenshot was not captured, but result is recorded as user runtime report.

### Important interpretation

Do **not** keep guessing additional save command names yet. POC-B/C/D prove the F6-to-virtual-NUMPAD-SUBTRACT helper works, but they do not prove that `ConsoleCommand(...)` itself is actually being executed in this retail build. Before interpreting the save commands as individually broken/gated, validate the console-command execution mechanism with a visible harmless canary.

Current canary artifact (local-only): **POC-E**, using:

`game.Savegame.Tools.Debug.TeleportPlayerToRestingPlace`

If POC-E visibly teleports the player, `ConsoleCommand(...)` execution works and the save commands are likely gated/rejected; next investigation should center on `AcceptSaveRequests` / `UnblockSaveController` / `SaveRequestController` semantics.

If POC-E does nothing, stop testing save commands through `ConsoleCommand(...)` and move to direct `SaveRequestController` / native-call investigation.

## Technical invariants

- Do not commit proprietary PAKs, vanilla extracted archives, saves, or local-only binary test artifacts.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists merely because it survives reload while the mod remains installed.
- Definition-only sockets remain runtime-dependent.
- Keep held-weapon drop and extra corpse-loot weapon rolls separate.
- Attack speed remains safety-sensitive.
- Scope loot-builder edits to exact named blocks; no ambiguous global first-match anchors.
- Test-delivery builds may be deterministic; final balance must return to frozen RNG targets.

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
6. Manual Save POC-B `ForcedAutosave` through current debug-command path.
7. Manual Save POC-C `PerformFullSave` through current debug-command path.
8. Manual Save POC-D `PerformFullSaveNoPreparation` through current debug-command path.

## next_safe_action

1. Keep POC-001 and POC-002 frozen green.
2. Run **Manual Save Console Canary POC-E** on disposable test save.
3. If teleport occurs, investigate save gating/controller state before any more save-command guesses.
4. If teleport does not occur, abandon `ConsoleCommand(...)` as the retail trigger path and investigate direct `SaveRequestController` native-call access.
5. In parallel, continue the smallest controlled Legendary -> L+1 persistent Ascension carrier POC without perturbing frozen-green paths.
