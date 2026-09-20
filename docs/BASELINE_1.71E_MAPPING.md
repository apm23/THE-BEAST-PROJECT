# Dying Light: The Beast 1.71E — Vanilla Mapping

This document records project-relevant observations from the clean 1.71E baseline supplied by the user. It intentionally records paths, semantics, and small facts only; original proprietary game files are not committed.

## Baseline acquisition

- Observed game version: `1.71E`.
- Clean install contained `data0.pak` and `data1.pak`.
- Targeted extraction completed: 58 requested files, 0 missing.

## Confirmed rarity/color mapping

`enums/item_color.def` exposes the color IDs. More importantly, `scripts/inventory/loot/lootpools_ft.loot` confirms gameplay meaning by named loot objects:

- Blue -> Rare (`Weapon_Rare` uses `ColorSet_BlueOnly`).
- Violet -> Epic (`Weapon_Epic` uses `ColorSet_VioletOnly`).
- Orange -> Legendary (`Weapon_*_Legendary` uses `ColorSet_OrangeOnly`).
- Platinum and Exotic exist above Orange in the enum/definitions, but are outside the initial Legendary target unless specifically needed later.

Therefore the project should treat **Orange as the native Legendary tier** for 1.71E.

## Weapon definition / affix architecture

Relevant paths:

- `scripts/inventory/inventory_weapondefintions_ft.scr`
- `scripts/inventory/inventory_gen.scr`
- `scripts/inventory/itemaffixes.scr`
- `scripts/inventory/loot/weaponprobpresets.scr`
- `scripts/inventory/loot/weaponsetpresets.scr`
- `scripts/inventory/loot/weaponscolorpresets.scr`

Observed behavior:

- Base weapon definitions carry a native `Color(...)`.
- Generated rank variants (`..._r1`, `..._r2`, etc.) carry `Rank`, `TierSpread`, stable `UID`, damage-tier linkage, drop/throw flags, dismantle tier, and explicit forced/random affix-group names.
- Lower-rarity generated weapons can hardcode Rare affix groups, e.g. `Slashing_1h_Affixes_Rare_ft` + `Weapons_Random_Rare_ft`.
- Native Legendary generated weapons exist and use Legendary-specific groups, e.g. `Slashing_1h_Affixes_Legendary_ft` + `Weapons_Random_Legendary_ft`.
- `itemaffixes.scr` defines Rare/Epic/Legendary named groups for multiple weapon classes, plus `Weapons_Random_Rare_ft`, `Weapons_Random_Epic_ft`, and `Weapons_Random_Legendary_ft`.

### Design consequence

A Universal Legendary implementation must not merely recolor a lower-rarity weapon. The controlled POC should create/route a real Orange item instance with Legendary affix groups and stable identity. This matches the project contract requirement that Legendary not be cosmetic-only.

## Human held-weapon generation/drop

Relevant path:

- `scripts/inventory/loot/weaponsetpresets.scr`

For the inspected standard human melee/bow/firearm weapon-set presets, `OverrideWeaponDropDurabilityParams()` already uses `LootChance(1.0)` for the held weapon, with durability ranges depending on weapon class.

### Design consequence

The earlier conceptual target of 60–75% held-weapon drop should **not** be applied blindly. On 1.71E, many standard human held weapons are already configured for 100% drop at this layer. Preserve vanilla 1.0 unless another upstream rule is shown to reduce it in practice. The needed change is primarily the rarity/native-instance roll, not lowering the held-weapon drop rate.

## Corpse loot: Biter / Viral / Human

Relevant path:

- `scripts/inventory/loot/lootpools_ft.loot`

### Biter

`LootedObject("Biter")` uses `ColorSet_DLC_FT_Enemy_Base`, has a large Empty/resource mix, and separately includes an `Enemy_Lottery_Weapons` roll under `ColorSet_OrangeOnly` with very small vanilla weight (`0.05`).

### Viral

`LootedObject("Viral")` similarly has a resource-heavy pool and a very small Orange-only `Enemy_Lottery_Weapons` roll (`0.05`).

### Human corpses

Standard `Human_1h`, `Human_2h`, and related corpse pools contain resources/cash/valuables plus a separate Orange-only `Enemy_Lottery_Weapons` roll with very small vanilla weight (`0.002`) for several classes. This is separate from the actual held-weapon drop described above.

### Design consequence

There are two independent human weapon paths to preserve:

1. actual held weapon drop;
2. extra corpse-loot weapon lottery.

Both can participate in Legendary gacha, but they should remain distinguishable in tuning/config.

## Color sets relevant to global gacha

Relevant path:

- `scripts/inventory/loot/color_sets.loot`

Important 1.71E sets include:

- `ColorSet_DLC_FT_Generic_Container`
- `ColorSet_DLC_FT_DH_Container`
- `ColorSet_DLC_FT_DH_Reward`
- `ColorSet_DLC_FT_HighRarity_Reward`
- `ColorSet_DLC_FT_Enemy_Base`
- `ColorSet_DLC_FT_Enemy_Advanced`
- weapon tier color sets (`ColorSet_WeaponT1/T2/T3`, endgame variants)
- infected-specific color sets

Vanilla already allows some Orange in container/reward sets, while base enemy sets are much lower. These are direct tuning points for the project’s global rarity-gacha layer.

## Weapon enhancement / upgrade mapping

Relevant paths:

- `scripts/inventory/weaponenhancmentcosts.scr`
- `scripts/crafting/crafting_effects.scr`
- `scripts/menu/menumodifyweapon.scr`

`weaponenhancmentcosts.scr` defines costs by weapon type and rarity, including Orange and Exotic. It does **not**, by itself, expose the complete stat-growth algorithm or a persistent arbitrary Ascension level.

`crafting_effects.scr` contains native passive effects for increased damage, durability, swing speed, and other combat stats, which may provide reusable native mechanisms for Ascension.

Ascension persistence remains unresolved and must not be claimed until tested.

## Controlled POC direction

The smallest useful proof should be one known lower-rarity FT melee weapon (initial candidate: the Opportunity axe family) cloned/routed into a true Orange/Legendary instance with:

- same model/name family;
- `Color_Orange`;
- Legendary forced affix group for its weapon class;
- `Weapons_Random_Legendary_ft`;
- stable unique item ID/UID;
- controlled, obvious loot source for testing;
- no global balance changes yet.

POC success criteria:

1. game boots;
2. test weapon appears;
3. UI recognizes it as Legendary/Orange;
4. Legendary affixes are actually used;
5. item can be picked up, dropped, stored, saved, reloaded;
6. after removing the POC PAK and loading a copied test save, persistence behavior is recorded exactly.
