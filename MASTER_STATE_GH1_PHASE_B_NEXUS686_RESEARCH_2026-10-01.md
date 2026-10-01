# GH1 Phase B — Nexus Mod 686 Research Note — 2026-10-01

Source inspected from user-supplied archive:
`Special Weapons Blueprints (Regular)-686-1-1-1766215481.zip`

Archive structure:
- outer ZIP contains `data5.pak`
- data5 SHA256: `599b225fabbac3601566858b0fda87426e643f92da6c10f425569d0fd9b06444`
- data5 contains only:
  - `scripts/inventory/collectables_ft.scr`
  - `scripts/trading/shop_item_sets.scr`

Important findings:

1. The mod does NOT implement pickup-triggered blueprint unlock. It primarily adds/defines weapon blueprints in `collectables_ft.scr` and exposes T1 blueprints through vendor item sets in `shop_item_sets.scr`.

2. Ten fully custom weapon blueprint families were found at the top of `collectables_ft.scr`, each with T1/T2/T3 definitions:
- The Legacy
- The Maimer
- The Duelist
- The Separator
- Medieval Mace
- Medieval Hammer
- Sanctuary
- Stiletto
- Zen
- The Goose

3. The blueprint definition pattern is valuable for GH1 clean-room reconstruction:
- `ItemType(ItemType_CraftPlan)`
- `CraftplanType("Weapon")`
- `ScaleWithPlayerRank("<weapon family>_r")`
- `ItemLevel(1,3)` / `(2,3)` / `(3,3)`
- `NextLevelBlueprintName(...)`
- T2/T3 use `RequiredItemToShowInShop(previous tier)` and upgrade-component AlternativePrice entries.
- rarity/color progression in this old file is Blue -> Violet -> Orange.

4. `shop_item_sets.scr` adds T1 blueprint IDs into `Hub1_Unlocks` and `Hub2_Unlocks`, meaning the mod's acquisition method is vendor exposure, not a weapon-pickup callback.

5. Current public Nexus comments show the old mod is stale on newer game versions. Reports on 1.6.2 describe lost interactions/stash access and force-close on quit. Therefore the user-supplied `data5.pak` MUST NOT be installed or copied wholesale into GH1 1.7.1.

6. Public author comments state that `collectables_ft.scr` must remain for newly-created blueprint definitions after purchase; `shop_item_sets.scr` can be removed after acquisition. Some weapons (e.g. Piercer / Cleaver / Hunting Knife according to the author discussion) already had Techland blueprint definitions and only needed exposure.

7. Design consequence for GH1 Phase B:
- keep the rejected mass weapon-definition `LinkedItems` strategy permanently rejected;
- do NOT ship the old Nexus full files;
- use current 1.7.1 effective files as source of truth;
- use the old mod only as a structural reference for how a missing native weapon blueprint can be defined cleanly;
- acquisition remains the user's new rule: only when a weapon is obtained from zombie loot, deliver/unlock its matching blueprint in the same loot event;
- first prove loot-event weapon+blueprint pairing on one native existing pair;
- after that, build clean-room blueprint definitions for weapon families that currently lack them, using the current game's own 1.7.1 craftplan conventions.

8. This old mod only proves/illustrates T1-T3 weapon blueprint progression. It does NOT prove Exotic/Iconic tiers or Legend 1-300 scaling. Those remain separate later research/test stages.

Status:
- RESEARCH ONLY
- no runtime GREEN claim from this archive
- do not install original data5 on current GH1
