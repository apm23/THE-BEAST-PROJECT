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
- V4 also confirmed `SaveGame(...)` / `SaveGameCtrl(...)` are logging config, not save-now commands.
- Collector V5 scanned engine/game binaries for filtered save-related strings without copying binaries.

Important V5 strings/classes include:

- `_ACTION_QUICK_SAVE`
- `MenuSaveLoad_InfoQuickSaveOK`
- `SaveController`
- `SaveRequestController`
- `SaveRequestHistory`
- `Savegame::Session::ESaveRequestPriority`
- `Savegame::Tools::ConsoleCommand::AcceptSaveRequests`
- `Savegame::Tools::ConsoleCommand::BlockSaves`
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

### Manual-save POC history

**POC-A — bind F5 to `_ACTION_QUICK_SAVE`: no observed save.**

- package installed successfully after CMD line-ending fix;
- F5 produced no watched save-file change;
- direct hidden action binding is rejected for now.

**POC-B/C/D — debug save command probes via virtual NUMPAD SUBTRACT: no watched save-file change.**

Tested strings:
- `game.Savegame.Tools.Debug.Save.ForcedAutosave`
- `game.Savegame.Tools.Debug.FullSave.PerformFullSave`
- `game.Savegame.Tools.Debug.FullSave.PerformFullSaveNoPreparation`

The F6 helper itself is proven: runtime screenshots showed F6 detected, foreground title `Dying Light: The Beast`, and virtual NUMPAD SUBTRACT sent to the active game window.

**POC-E — `TeleportPlayerToRestingPlace` ConsoleCommand canary: no teleport.**

This alone was not enough to conclude `ConsoleCommand(...)` is disabled, because the debugconf override itself had not yet been proven to load.

**POC-F — `debugconfdefault.scr` in `data2.pak` with `HideHUD()` load canary: FAIL TO LOAD.**

User supplied installed-vs-uninstalled gameplay screenshots. In both states the normal HUD remained visibly present: quest text, compass/safe-zone strip, health/stamina/item bar, world markers, and other HUD elements. Therefore `HideHUD()` from the `debugconfdefault.scr` packed inside `data2.pak` did not take effect.

### Critical interpretation after POC-F

- `data2.pak` itself is a valid mod-loading path for ordinary game scripts (proven by POC-001/002), but **the root `debugconfdefault.scr` is not being overridden from that PAK path in retail 1.71E**.
- Therefore POC-B/C/D/E must **not** be treated as proof that those ConsoleCommand strings themselves were executed and failed. The command script may simply never have been loaded.
- Stop interpreting those command probes until the actual debugconf load path is found.
- Do not guess more save command names yet.

### Current Manual Save artifact / next test

Local-only **POC-G — DebugConf Loose Source Canary** tests the most likely physical path:

`C:\Program Files (x86)\Steam\steamapps\common\Dying Light The Beast\ph_ft\source\debugconfdefault.scr`

POC-G installer:

- removes only the exact known POC-F `data2.pak` if present;
- reads the vanilla `debugconfdefault.scr` from the user's own `data0.pak` at install time;
- injects only a marker plus `HideHUD()`;
- writes the patched file as a physical loose file at `ph_ft\source\debugconfdefault.scr`;
- backs up any pre-existing physical loose file instead of overwriting it blindly;
- package contains no copied vanilla debugconf file.

Interpretation:

- HUD hidden after full restart -> the physical `ph_ft\source` debugconf path is real; use that path for a new ConsoleCommand canary and then save-controller research.
- HUD unchanged -> uninstall POC-G and test the next plausible physical load location (game executable/root directory), not more save commands.

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
- For Windows helper packages: user launches `.cmd`; `.cmd` only launches the `.ps1` and stays open with `pause`; install/uninstall logic lives in PowerShell.

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
6. `debugconfdefault.scr` override from inside `data2.pak` for retail debug commands / `HideHUD()`.

Note: POC-B/C/D/E are retained as **inconclusive command probes**, not frozen command failures, because POC-F proved the debugconf packed in `data2.pak` was not actually applied.

## next_safe_action

1. Keep POC-001 and POC-002 frozen green.
2. Run **POC-G DebugConf Loose Source Canary** after a full game shutdown/restart.
3. If HUD disappears, freeze `ph_ft\source\debugconfdefault.scr` as the actual physical debugconf load path and re-test one harmless ConsoleCommand canary through that path before save commands.
4. If HUD remains normal, uninstall POC-G and test the next physical debugconf candidate at game root/executable directory.
5. Do not resume save-command guesses until a debugconf execution path is proven.
6. In parallel, continue the smallest controlled Legendary -> L+1 persistent Ascension carrier POC without perturbing frozen-green paths.
