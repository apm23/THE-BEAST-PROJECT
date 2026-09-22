# PLAY NOW A1 + A2 + A3 — V3

Status: **LOCAL DISTRIBUTABLE BUILT / STATIC AUDIT PASS — awaiting in-game smoke test**

Target: Dying Light: The Beast **VER. 1.71E**.

This is the current fast-play package. It combines the user-locked A1 ammo economy, A2 enemy/human loot rebuild, and A3 inventory-capacity expansion. Deep Legendary Core / Ascension research remains a separate workstream.

## Safety decision: active weapon wheel

The user requested a target of eight equipped/active weapons, but safety is explicitly the top priority. V3 **does not force eight active weapon slots**. The mapped inventory capacity (`QuickSlotsCount`) is increased, while the visible/active wheel parameter (`VisibleQuickSlotsCount`) is intentionally left unchanged. Publicly mapped input actions consistently expose weapon SLOT1–SLOT4 only, so forcing 5–8 is deferred until a proven UI/input/save-safe path exists.

Result: total weapon inventory is enlarged to 300% of vanilla while active weapon selection remains at the proven vanilla four-slot behavior.

## A1 — ammo recipe balance

Standard firearm ammo is Scrap-only:

- Pistol: 10 Scrap -> 60
- Revolver: 14 Scrap -> 24
- SMG: 18 Scrap -> 120
- Shotgun: 24 Scrap -> 24
- Rifle: 30 Scrap -> 80
- Marksman: 37 Scrap -> 32

Special/native ammo:

- Arrow: 20 Scrap + 1 Feather -> 35
- Fire Arrow: 20 Scrap + 1 Resin + 1 Feather -> 35
- Shock Arrow: 30 Scrap + 1 Wiring + 1 Feather -> 35
- Bolt: 24 Scrap + 1 Feather -> 35
- Fire Bolt: 36 Scrap + 1 Alcohol + 1 Feather -> 35
- Shock Bolt: 36 Scrap + 1 Wiring + 1 Feather -> 35
- 40mm Electric: 20 Scrap + 1 Container + 1 Battery -> 35
- 40mm Explosive: 20 Scrap + 1 Container + 1 Battery -> 35
- 40mm Flashbang: 20 Scrap + 1 Container + 1 Cleaning Supplies -> 35
- 40mm Freeze: 20 Scrap + 1 Container + 1 Oxidizer -> 35
- 40mm Incendiary: 20 Scrap + 1 Container + 1 Fuel Can -> 35
- Sawblade: 40 Scrap + 1 Leather + 1 Blade -> 35
- Flamethrower: 1 Resin + 1 Fuel Can -> 800

The six standard recipes are project definitions. The installer patches the 13 native special-ammo craftplans from the user's own `data0.pak` / `data1.pak` at install time rather than redistributing proprietary vanilla source.

## A2 — full infected + human loot rebuild

V3 rebuilds the added loot layer for 28 mapped infected/human/boss corpse objects. Human corpse loot now participates in the modded system rather than feeling vanilla-only. Existing held-weapon logic remains separate from added corpse bonus loot.

### Scrap

When the rebuilt enemy/human resource path selects Scrap, the amount is at least 40. Mapped ranges:

- Base/Biter: 40–55
- Viral: 45–65
- Screamer: 50–70
- Human: 45–70
- Baron/elite-human resources: 55–80

The internal Scrap weight in those resource subpools is increased by 10%.

### Added loot probability targets per draw

Tier 0 ordinary Biter:
- Empty 8%
- firearm 4%
- melee 6%
- weapon-mod blueprint 12%
- actual ammo 8%
- Ammo Blueprint Pack 1%

Tier 1 Police/Viral/basic human:
- Empty 5%
- firearm 6%
- melee 8%
- mod 14%
- ammo 10%
- pack 1%

Tier 2 special infected/armed human:
- Empty 3%
- firearm 8%
- melee 10%
- mod 16%
- ammo 12%
- pack 0.8%

Tier 3 elite/boss:
- Empty 1%
- firearm 10%
- melee 12%
- mod 18%
- ammo 14%
- pack 0.5%

The remaining probability preserves the object's vanilla loot categories. Added category entries use `min_amount=1,max_amount=1`; a selected added category therefore cannot resolve to a deliberate zero-item amount.

### Weapon rarity after weapon category is selected

- Common 5%
- Rare 20%
- Epic 35%
- Legendary 40%

For a Legendary branch:
- **80% native-Legendary path**
- **20% promoted/expanded-Legendary path**

Native firearm Legendary uses explicit vanilla firearm families whose IDs contain the native `_legendary_` definitions; 75 rank-mapped item IDs were included in the static build. Native melee uses the vanilla `Enemy_Lottery_Weapons` Legendary-capable path. The goal is to make native/original Legendary drops dominate promoted Legendary drops.

### Weapon-mod blueprint tier after mod category is selected

- T1 10%
- T2 20%
- T3 30%
- T4 40%

Actual firearm/special ammunition is also present in the added corpse loot layer. The all-ammo blueprint pack remains deliberately rare to reduce redundant duplicate packs.

## A3 — inventory, ammo, stash

At install time, the package patches the user's own native `scripts/player/player_variables.scr`:

- `QuickSlotsCount`: **300% vanilla**, capped at 99; this is the total weapon inventory target.
- `AmmoSlotsCount`: **200% vanilla**, capped at 99 when present.
- mapped `Storage*SlotsCount` values: **200% vanilla** when present.
- native `MaxAmmoCountInventoryUpgrade(...)` values in ranged inventory definitions: **200% vanilla**, capped at 999.
- `VisibleQuickSlotsCount`: **not changed**.

General consumable inventory is not aggressively expanded.

## Installer / uninstaller safety

The user runs `RUN_INSTALL.cmd`; it launches the PowerShell installer and keeps the window open with an explicit exit code.

Installer behavior:
- requires game closed;
- backs up discovered Steam AppID 3008130 saves before changing the mod archive;
- backs up the previous known project `data2.pak` before replacement;
- recognizes known project V1/V2/POC hashes;
- **stops safely on an unknown `data2.pak`**;
- builds native A1 recipe/player-variable patches from the user's own game archives;
- writes an install-state JSON and runtime audit.

Uninstaller behavior:
- refuses to remove/restore if installed `data2.pak` no longer matches the recorded V3 hash;
- requires explicit `REMOVE` confirmation;
- warns the user to reduce weapon/ammo/stash contents below vanilla capacity first;
- restores the prior known-project `data2.pak` if one existed;
- keeps save backups.

## Static build result

Final local distributable ZIP SHA-256:

`4bc2b1c93c92ab269f4790a458e1ff89d267671844d5d3913b06605b01b322d5`

The package contains project-authored text/scripts only. No vanilla PAK, save, EXE, DLL, or proprietary extracted archive is committed to this repository.

Static gates passed:
- ZIP integrity;
- internal manifest hash verification;
- payload brace balance;
- exact six standard A1 recipes;
- all mapped A2 custom `use` targets resolve to defined subroutines;
- rebuilt Scrap minimum is >=40 in mapped resource subpools;
- 19 native ammo-cap triplets are doubled with cap <=999;
- no active weapon-wheel parameter is forced;
- no proprietary binary/save artifact exists in the distributable source payload.

**Runtime status remains NOT GREEN until the user installs V3 and completes the first normal-play smoke test.**

## First smoke test

1. Install with game closed and require `ExitCode=0`.
2. Launch and confirm inventory/UI opens normally and weapon inventory capacity is visibly larger.
3. Kill roughly 20–50 Biters and at least 10 humans; confirm corpse interaction remains normal, empty corpses are uncommon, Scrap drops are >=40 when selected, and ammo/mod/weapon variety appears.
4. Confirm native/original Legendary families appear more often over continued play and are not dominated by promoted lower-family weapons.
5. Craft at least one standard firearm ammo and one native/special ammo recipe and verify the requested A1 costs/outputs.
6. Save, quit, reload, and verify inventory/weapon/ammo state remains normal.
