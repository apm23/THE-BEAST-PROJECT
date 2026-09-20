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

**PHASE 1F — POC-001 and POC-002 are green. Native per-item installed-mod state, stat bonuses, visuals, and functional Toxic proc all survived save/reload and POC uninstall on the tested Camp Axe path.**

Global gacha, Legendary Core, full Ascension, and Manual Save Anywhere are not implemented yet.

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
- Common Biter weapon availability: **20–25%** final target, subject to loot semantics/inventory pressure.
- Human held-weapon drop: preserve confirmed vanilla `LootChance(1.0)` where present; extra corpse weapon lottery tuned separately.
- Legendary Core target chances: common infected 8–10%, Viral/human ~10%, special infected 12–15%, ordinary containers 8–10%, good/locked chest 12–15%, boss/Chimera 20–30%.
- Core costs: Rare/Epic->Legendary 1; L->L+1 1; +1->+2 2; +2->+3 3; +3->+4 5; +4->+5 8.

## Confirmed 1.71E mapping

See `docs/BASELINE_1.71E_MAPPING.md`.

- Blue = Rare; Violet = Epic; Orange = Legendary; Platinum/Exotic exist above Orange.
- Key files include `inventory_gen.scr`, `itemaffixes.scr`, `lootpools_ft.loot`, `lootsets_ft.loot`, `weaponprobpresets.scr`, `weaponscolorpresets.scr`, `weaponsetpresets.scr`, `weaponenhancmentcosts.scr`, and `crafting_effects.scr`.
- Native Legendary generation uses class-specific Legendary affix groups plus `Weapons_Random_Legendary_ft`.
- Lower-rarity weapons can hardcode Rare affix groups; Universal Legendary cannot be cosmetic-only.
- Standard inspected human weapon presets use held-weapon `LootChance(1.0)`.
- Vanilla `LootedObject("Biter")` has `LootAmount(2)` and a very large `Empty` path (`50.0` normal, `70.0` PermaWorld) before considering other resource pools.
- `ShockMod_PowerAttack_FT_T4` and `ShockMod_Random_FT_T4_TIP` are native Orange/T4 weapon mods.
- Direct loose `CategoryType_CraftPart` delivery through ordinary Biter corpse-resource loot is not proven and is currently rejected as a test-delivery mechanism.
- `StartupMod(...)` is a confirmed native generation mechanism used by vanilla generated weapons.

## POC-001 — Native Legendary Opportunity/Camp Axe

Local-only artifact SHA-256:
`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

Confirmed runtime result:

- Camp Axe generated as **Legendary One-Handed Axe** from a vanilla Rare-path definition.
- Legendary identity, affixes, damage `131`, durability `160/160`, and repairs `7/7` survived save/reload and survived POC removal.
- Definition-added Tip/Shaft/Grip sockets did **not** survive uninstall; only vanilla Charm Socket remained.

Frozen conclusion: rarity/affixes/damage/durability/repair count can persist per item strongly enough to survive mod removal; definition-only socket structure cannot be assumed persistent.

## POC-002 — Persistent native installed-mod probe

Goal: determine whether a native installed weapon mod and its stat/effect state persist across save/reload and uninstall even when the socket itself only exists while the POC definition is installed.

### Rejected delivery iterations

- Initial POC-002 custom Biter loot subroutine removed corpse `F` interaction. Rejected.
- POC-002B patched the wrong resource subroutine because of an ambiguous global anchor. Rejected.
- POC-002C correctly patched `Biter_CommonResources`, but outer vanilla Biter loot produced too many `Nothing` results for focused testing. Rejected as impractical.
- POC-002D forced the outer resource path and removed `Nothing`, but Shock T4 still never materialized as a loose CraftPart. Direct loose-mod-through-Biter-resource delivery is rejected.
- POC-002E uses `StartupMod("ShockMod_Random_FT_T4_TIP")` on a generated test axe and remains a valid fallback, but it was not needed for the successful persistence probe below.

### Manual Venom/Poison persistence test — confirmed runtime evidence

The user owned a native Poison/Venom weapon mod and manually installed it into the exposed Tip Socket of the same Legendary Camp Axe.

**Before installing Venom:**

- rarity: **Legendary One-Handed Axe**;
- damage: **131 Slashing Damage / 131 Base Damage**;
- affixes: `+33% Damage (Melee Weapon Throw)`, `+6% Damage (Infected)`, `-7.5% Stamina Cost (Melee Weapons)`;
- durability: **160/160**;
- repairs: **7/7**;
- Tip, Shaft, Grip, Charm sockets visible and empty.

**Immediately after installing Venom into Tip Socket:**

- visible installed mod/effect: **Venom — Applies TOXIC on critical hits**;
- damage: **137 Slashing Damage / 137 Base Damage**;
- durability: **185/185**;
- repairs: **7/7**;
- Legendary rarity and all three rolled affixes unchanged;
- damage delta: `131 -> 137` (`+6`);
- durability delta: `160 -> 185` (`+25`).

**Save -> quit -> reload with POC still installed:** PASS.

The exact same axe still showed:

- **137 damage**;
- **185/185 durability**;
- **7/7 repairs**;
- visible **Venom** entry and Toxic description;
- same Legendary rarity and same rolled affixes.

**After uninstalling the POC and loading vanilla 1.71E:** PASS.

Observed after uninstall:

- rarity still **Legendary One-Handed Axe**;
- damage still **137**;
- durability still **185/185**;
- repairs still **7/7**;
- original three rolled affixes still present;
- Tip/Shaft/Grip socket UI disappeared exactly as expected from POC-001; only vanilla **Charm Socket** remains;
- the Venom hardware/model remained visibly attached to the axe and the green poison visual remained visible;
- the side-panel Venom row was no longer shown because the Tip Socket itself is no longer exposed by the vanilla weapon definition.

**Functional combat check after uninstall:** PASS.

While still fully vanilla after uninstall, the same Camp Axe continued to trigger the Toxic/Venom combat effect on infected. The user directly compared the observed effect against another weapon that natively has Toxic and reported the effect behaved the same.

### POC-002 conclusion — FROZEN GREEN

POC-002 is now fully green for the tested Venom-on-Camp-Axe path:

1. A native weapon mod installed on a per-item basis survives save/reload.
2. Its stat changes survive removal of the mod package that exposed the socket: **+6 damage and +25 durability remained after uninstall**.
3. The installed mod's visual attachment/effect remains on the item after uninstall even though the definition-added Tip Socket disappears from the UI.
4. The actual Toxic combat proc remains functional after uninstall.
5. Therefore installed native mod/effect state is serialized independently enough from the live weapon socket definition to remain functional on the item/save.
6. This is a strong technical foundation for persistent Ascension if L+1..L+5 can be encoded using native invisible/startup mods or equivalent persistent per-item crafting/effect carriers.
7. Do not use definition-only extra sockets themselves as the Ascension state marker; those are still proven runtime-dependent.

## Manual Save Anywhere

Feature is frozen in `FEATURE_SPEC.md`, but implementation is pending native save-trigger mapping.

Collector V2 failed before extraction due a PowerShell path parsing bug. Collector V3 was built to enumerate archive paths first and broadly collect save/checkpoint/input/state/invoke candidates. No claim of a working F5 save exists yet.

## Technical invariants

- Do not commit proprietary PAKs, vanilla extracted archives, saves, or local-only binary test artifacts.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never fake Legendary via text/color only.
- Never assume a property persists merely because it survives reload while the mod remains installed.
- Treat definition-only sockets/structure as runtime-dependent unless separately proven persistent.
- Keep held-weapon drop and extra corpse-loot weapon rolls separate.
- Attack speed remains safety-sensitive.
- Scope loot-builder edits to exact named sub/object blocks; do not use ambiguous global first-match anchors.
- Test-delivery builds may be deterministic; final game balance must return to the frozen RNG targets.
- Do not keep tuning loot weights after a runtime result proves the targeted delivery mechanism itself is not materializing the intended item class.

## Frozen-green systems

- **POC-001 native Legendary identity:** GREEN.
- **Persistence of rarity/affixes/damage/durability/repair count after uninstall:** GREEN for tested Camp Axe path.
- **Definition-added extra sockets after uninstall:** confirmed NOT persistent.
- **POC-002 native installed-mod stat persistence:** GREEN for tested Venom-on-Camp-Axe path (`137` damage and `185/185` durability persisted after uninstall).
- **Installed Venom visual attachment after uninstall:** GREEN for tested path.
- **Functional Toxic proc after uninstall:** GREEN for tested path.

## Failed hypotheses / rejected implementations

1. Custom POC-002 Biter loot subroutine: rejected after corpse loot interaction disappeared.
2. POC-002B global first-match resource-anchor patching: rejected; wrong subroutine was modified.
3. POC-002C inner-weight-only delivery: rejected for focused testing because outer vanilla Biter RNG still produced too many `Nothing` outcomes.
4. POC-002D direct loose Shock CraftPart through forced `Biter_CommonResources`: rejected after runtime showed non-empty loot but still no Shock item.

## next_safe_action

**Pivot from persistence discovery to the smallest Ascension stage-carrier POC, while Manual Save Anywhere mapping may continue in parallel.**

1. Keep POC-001 and POC-002 frozen green; do not perturb their proven paths.
2. Investigate the smallest native invisible/startup-mod or crafting-effect carrier that can encode one controlled **Legendary -> L+1** upgrade on a single weapon instance without depending on a persistent visible socket.
3. First L+1 POC should target only the already-tested Camp Axe path and should change damage/durability by a clearly measurable amount while preserving rarity, affixes, repairs, identity, and hit behavior.
4. Save/reload and uninstall-test that L+1 carrier exactly as with POC-002.
5. Only after one L+1 carrier survives should extend the same mechanism to L+2..L+5 and then wire Legendary Core costs/UI around it.
6. Manual Save Anywhere mapping may continue in parallel, but do not claim it implemented until a native save trigger is confirmed.
