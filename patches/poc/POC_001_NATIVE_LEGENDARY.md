# POC-001 — Native Legendary Opportunity Axe

Status: **BUILT — awaiting in-game validation**

Target: Dying Light: The Beast **1.71E** clean baseline.

This POC is intentionally small. It does not implement the final global gacha, Legendary Core, or Ascension system. Its only purpose is to prove that a weapon family which is lower-rarity in vanilla can be instantiated as a real Orange/Legendary item with Legendary affix groups and then tested for save persistence.

## Test weapon

Existing generated item:

`dlc_ft_WPN_1HS_AXE_03_opportunity_r1`

The POC preserves the original item name, visual identity, and UID so uninstall testing can reveal whether the save persists item-instance rarity/affix state or whether the game recomputes those properties from vanilla definitions.

## Patch behavior

### `scripts/inventory/inventory_gen.scr`

Only the `dlc_ft_WPN_1HS_AXE_03_opportunity_r1` block is changed:

- adds `Color(Color_Orange)`;
- adds four crafting slots;
- changes forced affix group from Rare to `Slashing_1h_Affixes_Legendary_ft`;
- changes random affix group from Rare to `Weapons_Random_Legendary_ft`;
- changes dismantle result from T1 Slash to T3 Slash.

No other rank of this weapon is changed in POC-001.

### `scripts/inventory/loot/lootsets_ft.loot`

`Enemy_Lottery_Weapons` is temporarily reduced to one deterministic test item:

`dlc_ft_WPN_1HS_AXE_03_opportunity_r1`

This is test-only. The final mod must restore the normal weapon pool and implement the agreed rarity gacha instead.

### `scripts/inventory/loot/lootpools_ft.loot`

Only the ordinary `Biter` loot object is changed. Its two existing `Enemy_Lottery_Weapons` calls (normal and PermaWorld branch) are raised from weight `0.05` to `15.0` so the POC item can be obtained quickly from ordinary Biters without making every kill deterministic.

No Viral, human, container, boss, or global color-set balance is changed by POC-001.

## Built artifact

Local artifact name: `data2.pak`

SHA-256:

`b707f6918c83dc5962dc24695c63b94244f1f9d77eec2af9be37fed9ceaa5659`

The PAK contains exactly three paths:

- `scripts/inventory/inventory_gen.scr`
- `scripts/inventory/loot/lootsets_ft.loot`
- `scripts/inventory/loot/lootpools_ft.loot`

Static checks performed before packaging:

- ZIP/PAK integrity check passed;
- brace counts remain balanced and equal to the vanilla source files;
- no UTF-8 BOM was introduced;
- original CRLF line-ending format was preserved.

## Required in-game validation

Use only a test save.

1. Install POC `data2.pak`.
2. Launch game and confirm no startup/load error.
3. Kill and loot ordinary Biters until the Opportunity axe appears.
4. Confirm the item is displayed as Orange/Legendary and actually carries Legendary-style affixes/mod slots rather than only a color change.
5. Save, quit, and reload while the POC remains installed; confirm the weapon remains valid.
6. Back up the changed test save.
7. Remove only this POC `data2.pak`.
8. Reload the copied test save in clean vanilla and inspect the exact same weapon.
9. Record whether rarity, affixes, crafting slots, damage/durability, and inventory validity persist or revert.

Do not advance to global rarity/drop changes until this result is recorded in `MASTER_STATE.md`.
