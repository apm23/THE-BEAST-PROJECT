# MASTER INSTALLED MOD MANIFEST — 2026-10-01

## Purpose

This file records the **actual Dying Light: The Beast mod stack installed on the user's PC** as observed by the read-only audit `DLTB_CURRENT_MOD_AUDIT_20261001_092107.zip`.

This manifest is the source of truth for future consolidation/reinstall work. Historical proven mods that are not present in this audit must **not** be silently added to the reinstall bundle.

Target future workflow:

`fresh vanilla DLTB -> one consolidated reinstall bundle -> same effective functions as this audited stack`

Prefer a single consolidated `data4.pak` over modifying vanilla `data0-data3` directly, but preserve exact behavior first and simplify only after per-feature verification.

---

# Active PAK state

- `data0.pak` — vanilla slot, size 108034290
- `data1.pak` — vanilla slot, size 201264780
- `data2.pak`
  - size: 75554
  - SHA256: `534d30b8ec22a51cd5bf24dc5118a010c0b6752b1b2386ffdad3b72cfe3dbe00`
- `data3.pak`
  - size: 227082
  - SHA256: `39da0f1bbbf6ea6b785ba1313629b853161514d428ffe786ed8fb81d51ec548e`
  - exact match: structurally repaired current data3 baseline created during SP1
- `data4.pak`
  - size: 32249
  - SHA256: `e12fe4f7a4729b3857cf17f9a25c958f01efe749d4ad6ddb7096d1471fdc5eb6`
  - exact match: `DLTB_SURVIVOR_SENSE_MASTER_V2_CYAN_INSTANT_PERSIST_READY.zip`

No inactive/backup PAK-like files were found in the active source directory by this audit.

---

# Loose override

One relevant loose script override is present:

`ph_ft/source/data/ailife/generated/generated_scenario_tags.scr`

- size: 7184
- SHA256: `429c4de862888cb1778b2246b047fcffc5a48036ece8c9c240aad22b5e45dbaf`

This same loose override was present in the historical 2026-09-25 live-state snapshot.

Status: **UNRESOLVED / PRESERVE**.

Do not delete or omit it from a future reinstall until its delta against vanilla `data0.pak/ailife/generated/generated_scenario_tags.scr` is understood.

---

# Effective precedence note

The current `data2.pak` contains custom loot filenames:

- `scripts/inventory/loot/default.loot`
- `scripts/inventory/loot/tbp_lootpools_global_v1.loot`
- `scripts/inventory/loot/tbp_lootsets_global_v1.loot`

However current `data3.pak` contains the same two custom `tbp_*` filenames at a higher PAK precedence.

Therefore the **effective custom loot implementation at runtime is the data3 version**, not the data2 copy.

Do not rebuild the final stack by blindly taking `data2` loot payload as authoritative.

---

# CURRENT INSTALLED FUNCTIONS

## 1. Inventory capacity expansion — INSTALLED

Source currently present in `data2` and preserved by current `data4` player variables merge.

Observed effective values include:

- `MaxEquipmentSlotsCount = 34`
- `EquipmentSlotsCount = 34`
- `MaxConsumableSlotsCount = 34`
- `ConsumableSlotsCount = 34`
- `MaxQuickSlotsCount = 68`
- expanded storage equipment/consumable capacities up to 100 in the current player variable payload

Relevant current files:

- `scripts/player/player_variables.scr`
- `scripts/skills/common_skills.xml`

Status: **CURRENT-INSTALLED / SOURCE PRESERVED**.

Current Sense V2 also overrides `scripts/player/player_variables.scr`, but was built from the active data2 baseline and preserves these inventory values.

---

## 2. Custom armor / outfit tuning — INSTALLED

Current repaired `data3` contains custom XP-farm outfit definitions and affix behavior.

Relevant files include:

- `scripts/inventory/inventory_outfits_ft.scr`
- `scripts/inventory/itemaffixes.scr`

Observed examples:

- `OutfitPartForcedAffixGroup("Outfits_XPfarm_Affixes_ft")`
- explicit `OutfitArmor(...)`
- explicit `ScaledOutfitArmor(...)` progression for outfit pieces

This content also matches older project symbol reports where these XP-farm outfit definitions were already part of the effective modded runtime.

Status: **CURRENT-INSTALLED / HISTORICAL PROJECT LINEAGE MATCH**.

Exact standalone package name is not yet isolated, so the current repaired data3 content is the canonical source for consolidation.

---

## 3. Resource quantity + merged high-loot/G1/SPECIAL45 lineage — INSTALLED

The current effective data3 custom loot files contain project markers and resource modifications.

Effective files:

- `scripts/inventory/loot/tbp_lootpools_global_v1.loot`
- `scripts/inventory/loot/tbp_lootsets_global_v1.loot`

Current data3 marker counts/behavior identify this as a merged descendant of the historical `USER_HIGH_LOOT_SPECIAL45` / G1 payload.

Observed resource quantities include:

- Scrap commonly `40..55`
- ordinary crafting resources commonly `33..50`
- firearm scrap commonly `15..25`

Observed project routes include:

- `DLTB_PlayNow_*`
- `DLTB_G1_Firearm_ExoticNative`
- rarity/weapon branches on special infected/humans
- mod-blueprint routes
- ammo-blueprint bundle routes
- `DLTB_G1_NightSovereignBundle`
- `DLTB_G1_Charms`

Status: **CURRENT-INSTALLED / STRONG LINEAGE MATCH TO USER_HIGH_LOOT_SPECIAL45 + G1**.

Important: do not substitute the old historical `DLTB_ONECLICK_USER_HIGH_LOOT_SPECIAL45.zip` wholesale. The current installed files are a newer merged state and have different hashes. Use current data3 as canonical behavior, and use the old artifact only as lineage/reference during reconstruction.

---

## 4. Flashlight mod — INSTALLED

Current repaired `data3` contains a clear JovianStone flashlight modification.

Primary file:

`data/flashlightcolorgradingoverridepresets.scr`

Observed preset:

`FlashlightColorGradingOverridePreset("BiggerFlashlightForDarkerColorGrading")`

Observed edits include comments such as:

- `JovianStone edited from 2;3;4`
- near size changed from `3.8` to `6.5`
- far size changed from `0.2` to `1.0`

Related varlist/highlight files are also present in data3.

Status: **CURRENT-INSTALLED / AUTHOR MARKER = JovianStone / STANDALONE PACKAGE NOT YET MATCHED**.

For future consolidation, current repaired data3 is the canonical exact source unless the original standalone package is later identified.

---

## 5. Silent / reduced-noise firearm mod — INSTALLED

Current repaired `data3` contains clear Syxsta markers in firearm definitions.

Primary files include:

- `scripts/inventory/inventory_firearmsdefintions.scr`
- `scripts/inventory/inventory_weapondefintions.scr`

Observed modifications include repeated:

- `NoiseDataUid("noise_bow"); // Syxsta`
- `AINoiseDataUid("noise_bow"); // Syxsta`

This is an AI-noise/silent-firearm style patch.

Status: **CURRENT-INSTALLED / AUTHOR MARKER = Syxsta / STANDALONE PACKAGE NOT YET MATCHED**.

For future consolidation, current repaired data3 is the canonical exact source unless the original standalone package is later identified.

---

## 6. Broad all-infected / all-AI Survivor Sense edits — INSTALLED

Current repaired `data3` contains a broad older TBP Sense patch across many human-AI definition files.

Observed marker families include:

- `TBP V5 ALL INFECTED`
- `TBP V9`
- `TBP GOLDEN V4`

Typical inserted fields include:

- `m_XrayEnabled = 1`
- `m_SurvivorSensePreset = Preset_red_FT`

This older broad patch is distinct from the newer Biter empty-hostility fallback.

Status: **CURRENT-INSTALLED / TBP PROJECT SOURCE PRESERVED IN REPAIRED DATA3**.

Do not assume this broad static patch alone controls ordinary Biter Sense; SP1 proved ordinary Biter required the empty-hostility fallback.

---

## 7. Native Biter Survivor Sense / XRay — INSTALLED

Proven mechanism:

`SurvivorSenseHostilityPresets("")` empty-key fallback for hostile AI.

Runtime-proven effects:

- ordinary Biter native through-wall highlight
- sleeping/resting Biter native through-wall highlight

Current data4 is the newer Sense V2 test package:

SHA256 `e12fe4f7a4729b3857cf17f9a25c958f01efe749d4ad6ddb7096d1471fdc5eb6`

Proven part:

- empty-hostility fallback route
- resting/sleeping Biter support

Test-pending parts:

- cyan color behavior
- near-zero fade-in
- 60-second persistence
- 400m post-detection visibility

Historical minimal proven red Biter Sense data4 SHA256:

`8b0989886622cde9ef9ee1464494bdfeec1a4efd22d2f51c8ae06e072565946b`

Status: **CURRENT-INSTALLED; CORE PROVEN, V2 ENHANCEMENTS TEST-PENDING**.

---

## 8. G1 Night Sovereign / charms — DETECTED INSTALLED EXTRA

Current data3 loot + inventory files contain:

- `DLTB_G1_NightSovereignBundle`
- `DLTB_G1_Charms`
- `Night_Sovereign` markers in inventory/affix content

This means the live install contains more than the five user-remembered mods.

Status: **CURRENT-INSTALLED / G1 PROJECT LINEAGE**.

Preserve these during consolidation unless the user explicitly asks to remove them.

---

# Current data2 exact members

`data2.pak` SHA256:
`534d30b8ec22a51cd5bf24dc5118a010c0b6752b1b2386ffdad3b72cfe3dbe00`

Members:

1. `scripts/inventory/loot/default.loot`
   - SHA256 `d9de64e82d2a0c204a0b673523892249a3b788ddc446ce55fe7f642cc29e0d9c`
2. `scripts/inventory/loot/tbp_lootpools_global_v1.loot`
   - SHA256 `25675f685cb91b1bfb87524e7c0486ba8a5330b3d9ced1e9214fb8dcf535ab47`
3. `scripts/inventory/loot/tbp_lootsets_global_v1.loot`
   - SHA256 `99016ff0a3df38384f69efbcf98075083f1cd3e2dcf29f37d47b894812ffad8a`
4. `scripts/player/player_variables.scr`
   - SHA256 `7aa41852dbbc97b284b67702f06d9e2b3fa9304b6d7ef9c24ae564434ba54f36`
5. `scripts/skills/common_skills.xml`
   - SHA256 `3d0ff19404a90792270b834d527de7ff3fe42348d7158c754e38b8c76b3db7ed`

---

# Current data3 effective custom-loot members

Because data3 wins over data2 for matching custom file paths:

- `scripts/inventory/loot/tbp_lootpools_global_v1.loot`
  - SHA256 `db0ed3eb485137cd591e7bfe336471e95e7f752b12f1da7de0c05b19fa6f6a61`
- `scripts/inventory/loot/tbp_lootsets_global_v1.loot`
  - SHA256 `d7e27c78fb9fff7169bfa1a6a615991b20bf268eb18da12d937d1aa40cf1882b`

These are the canonical currently-effective loot sources for future consolidation.

---

# Source matching summary

### Exact artifact/source match

- repaired current data3: exact SHA match to SP1 repaired artifact
- current Sense V2 data4: exact SHA match to generated Sense V2 artifact
- proven minimal red Biter Sense: exact historical artifact/hash known

### Strong project-lineage match, current files must remain canonical

- resource/high-loot/SPECIAL45/G1 stack
- custom XP-farm armor/outfit stack
- broad TBP all-infected Sense edits

### Installed with author marker but standalone package not yet identified

- JovianStone flashlight mod
- Syxsta silent/reduced-noise firearm mod

### Unresolved

- loose `data/ailife/generated/generated_scenario_tags.scr`

---

# Reinstall-consolidation rules

1. Treat this audit as the **gold current installed stack**.
2. Do not add historical proven mods merely because they existed in older project states.
3. Do not replace current merged loot with the old SPECIAL45 artifact wholesale.
4. Reconstruct from the currently-effective script content first; use old artifacts only to explain lineage or recover missing pieces.
5. Keep inventory values while merging current Sense `player_variables.scr`.
6. Preserve custom armor, flashlight, silent firearm, resource/high-loot/G1, broad static Sense, and proven Biter empty-hostility fallback unless explicitly removed by user.
7. Resolve or explicitly preserve the loose `generated_scenario_tags.scr` override before declaring the reinstall bundle complete.
8. Final target should preferably be a single `data4.pak` over fresh official `data0-data3`, but only if identical behavior can be reproduced without precedence regressions.
9. Verify final consolidated build feature-by-feature:
   - inventory capacity
   - custom armor/affix behavior
   - resource quantities
   - high-loot/SPECIAL45/G1 routes
   - flashlight
   - silent firearm AI-noise behavior
   - broad Sense targets
   - ordinary Biter Sense
   - sleeping/resting Biter Sense
   - Sense V2 cyan/fade/persistence only if those pending behaviors are later confirmed
10. Store final consolidated PAK SHA256 and per-file SHA256s in this manifest once runtime verified.

---

# Current status

**AUDIT MAPPING COMPLETE ENOUGH TO BEGIN CONSOLIDATION DESIGN.**

Do not yet delete the existing working `data2/data3/data4` stack. The current installed stack remains the rollback/reference baseline until a consolidated reinstall bundle passes runtime verification.
