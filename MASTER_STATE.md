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

**PHASE 1F — POC-001 and POC-002 are frozen green. Weapon POC-003 runtime is complete: with-POC reload passed, but its deliberately non-vanilla L+1 stat signature did not survive POC removal. Weapon research now pivots to a different serialized per-item Ascension field/carrier. Manual Save Anywhere remains PAUSED / CLOSED TEMPORARILY by user decision.**

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
12. Manual Save Anywhere remains a project idea but is **PAUSED** and must not consume further test cycles until explicitly reopened by the user.

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

Frozen conclusion: native installed per-item mod/effect state, stat changes, visual attachment, and functional effect can serialize strongly enough to survive removal of the POC that exposed the socket. This remains useful, but POC-003 proved that arbitrary replacement of the carrier's definition-level stat magnitude is not itself serialized per item.

## POC-003 — Legendary -> L+1 persistent carrier probe — RUNTIME COMPLETE / CUSTOM STAT SIGNATURE FAILED UNINSTALL

Project-authored builder:
`tools/build_poc003_l1_carrier.py`

Detailed test contract/result:
`patches/poc/POC_003_L1_CARRIER.md`

Runtime record:
`tests/results/POC_003_RUNTIME_UNINSTALL_RESULT.md`

Local-only `data2.pak` SHA-256:
`5608ecb1336ca84c80bc1472000ab9b50eb79a94a8a6a6c1b127f370cd31e17a`

Local user-test package SHA-256:
`a1eee27144a7ac612d0600bce57fa117d3ea8a915ca8ca258ae1615b13655a59`

POC design:

- generate a **new** Legendary Camp Axe through the controlled POC-001 acquisition path;
- attach native `ShockMod_Random_FT_T4_TIP` via `StartupMod(...)`;
- temporarily give that carrier a deliberately non-vanilla signature:
  - `CraftingEffect_IncreasedDamageMul` level **8**;
  - `CraftingEffect_IncreasedDurability` level **3** (`+18%`);
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

## Manual Save Anywhere research — PAUSED / CLOSED TEMPORARILY

User decision on 2026-09-22: **stop Manual Save Anywhere work for now. Do not continue collectors, native hooks, position-restoration experiments, or extra user test cycles unless the user explicitly reopens this feature.**

### What was actually proven

- DebugConf/ConsoleCommand was tested through packed, loose, EXE-adjacent, and explicit `-debugconf=` routes; visible `HideHUD()` canaries never executed. This route is a frozen dead end for retail 1.71E.
- Native binary mapping V7–V11 recovered real save-system structures and call paths in `gamedll_ph_x64_rwdi.dll`, including `SaveController`, `SaveRequestController`, their vtables, the native save dispatcher, quick-save selector behavior, and the game's own caller setup.
- The runtime helper was refined through POC-J/J2/J3/J4:
  - J2 fixed disappearing error output by keeping PowerShell in the same CMD;
  - J3 fixed the reserved PowerShell `$PID` collision;
  - J4 fixed process discovery by selecting `DyingLightGame_TheBeast_x64_rwdi.exe` instead of relying on window title.
- POC-J4 successfully found and validated exactly one active `SaveController` object, backed up the test save, armed the controller on F5, and observed the real Steam save file change immediately afterward.
- The successful F5 sequence showed native controller state transition from inactive to armed and then back to inactive after the engine processed it; the watched `save_ft_0.sav` changed in the same trigger window.

### What remains unresolved

- The F5-native trigger is therefore a **real save-file-write proof**, but it has **not** been accepted as a complete Save Anywhere feature.
- Inventory/progression persistence is not sufficient proof because vanilla saves those normally.
- Exact last-player-position restoration was not established to the user's satisfaction.
- A possible future implementation could pair the native save with explicit position/rotation/map capture and post-load restoration, but the user chose not to pursue that now.

### Frozen conclusion

Manual Save Anywhere is **not GREEN**, **not deleted**, and **not an active workstream**. Preserve all findings for a possible future reopen, but spend zero further development/test effort on it until explicitly requested.

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
- **POC-003 with-POC save/reload:** PASS.
- **POC-003 arbitrary custom L+1 stat signature after uninstall:** NOT persistent / NOT GREEN.
- **Manual Save Anywhere:** PAUSED / NOT GREEN. Native F5 save-file write is proven, exact position behavior unresolved.

## Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine.
2. POC-002B ambiguous global anchor.
3. POC-002C inner-weight-only test delivery.
4. POC-002D loose CraftPart through Biter resources.
5. POC-003 temporary native CraftPart parameter override as an arbitrary uninstall-persistent Ascension magnitude carrier.
6. Manual Save POC-A direct `_ACTION_QUICK_SAVE` binding.
7. `debugconfdefault.scr` override from inside `data2.pak`.
8. physical `ph_ft\source\debugconfdefault.scr` as a reliable retail DebugConf load path.
9. physical EXE-adjacent `debugconfdefault.scr` as a reliable retail DebugConf load path.
10. explicit `debugconf.scr` + `-debugconf=` as a reliable retail runtime route for this mod.

POC-B/C/D/E remain **inconclusive command probes**, not proof that the underlying native save functions themselves fail.

## next_safe_action

1. Keep POC-001 and POC-002 frozen green.
2. **Manual Save Anywhere stays paused. Do not resume it without an explicit user request.**
3. Treat POC-003's custom parameter-override carrier strategy as rejected for arbitrary persistent Ascension magnitude; do not build L+2..L+5 from it.
4. Weapon track: inspect the extracted 1.71E weapon/save-related definitions for a different **per-item serialized** quantity/state that can encode L+1 independently for two copies of the same weapon.
5. Prefer a field that already survives definition removal or whose numeric magnitude is item-instance data; avoid another global definition-only multiplier.
6. Build the next smallest L+1 POC only after that serialized candidate is mapped. Full Legendary Core remains blocked until a viable per-item Ascension state is proven.
