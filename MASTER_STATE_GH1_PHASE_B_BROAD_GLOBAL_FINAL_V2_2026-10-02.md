# GH1 Phase B — Generated Pair Runtime Proof + Broad Global Final V2 — 2026-10-02

## Runtime proof received

The generated-only Global Proof V2 produced repeated weapon+blueprint packages in runtime. User-observed pairs:

1. Pistol K13
2. .38 Revolver
3. Steel Bat
4. Tonfa
5. C15 Rifle
6. Skull Cracker
7. Sunray Pistol
8. The Elite Pistol

All observed weapons arrived together with their matching blueprint in the proof package.

Conclusion:
- GLOBAL `tbp_*` route is runtime active.
- weapon+matching-blueprint bundle delivery is runtime proven.
- generated blueprint acquisition path is runtime proven strongly enough to proceed beyond generated-only POC gating.
- save/reload persistence remains a separate check unless explicitly confirmed by the user.
- the repeated small rotation is expected from Generated-Only Proof V2 because that proof intentionally selected a small subset (max 6 firearm + 6 melee generated families) to make the test decisive.

## Problem now addressed

The next problem is no longer blueprint pairing. It is final loot breadth / repetition.

The user explicitly reported the proof loot rotating through the same small set repeatedly. Therefore Final V2 removes the proof subset restriction and rebuilds the paired global weapon selector from the complete currently installed Global V1 pair set.

## Artifact

`GH1_PHASE_B_BROAD_GLOBAL_FINAL_V2.zip`

Package SHA256:
`14155176ea0678b98e0f4a49fbc28b7f5e013124f6be9e7e0cbd721df00e7e3a`

Core Python SHA256:
`35f1b3b358c841f73028c3d3164252c6e8fb2d90f7d55ee6b3ddb00365a7c5f2`

## Broad Final V2 architecture

Locked global route remains:

`default.loot -> tbp_lootpools_global_v1.loot -> tbp_lootsets_global_v1.loot`

Do NOT return to isolated/local vanilla loot routes.
Do NOT mass-edit weapon definitions.
Do NOT use the rejected `LinkedItems` approach.

Final V2 dynamically reads the current installed Global V1 stack and:

1. Resolves the effective current versions of:
   - `scripts/inventory/collectables_ft.scr`
   - `scripts/inventory/loot/tbp_lootpools_global_v1.loot`
   - `scripts/inventory/loot/tbp_lootsets_global_v1.loot`
2. Parses every existing weapon+matching-blueprint `ItemBundle` pair, native and generated.
3. Resolves the current paired lootset pool memberships.
4. For every one of the 16 target infected, creates a dedicated BROAD selector for NORMAL and PERMA (32 selectors total).
5. Preserves each infected section's current paired weapon rarity/source route shares.
6. Inside each existing rarity/source route, equalizes by weapon family instead of letting raw bundle/rank row count bias selection.
7. Merges the paired weapon routes into one broad selector per section while zeroing the redundant paired calls inside that section.
8. Applies a moderate total paired-weapon route boost of x1.50 so weapon loot is more noticeable without using proof-level forced weights.
9. Leaves resource, charm and Night Sovereign routes untouched.
10. Writes a fresh highest-number `dataN.pak` overlay; existing lower project/mod PAKs are not overwritten.
11. If the exact known Generated-Only Proof V2 overlay is still installed, the Final V2 installer removes only that marker-owned temporary proof overlay before resolving the underlying Global V1 files.
12. Writes runtime audit report:
    `Documents\GH1_PHASE_B_BROAD_GLOBAL_FINAL_V2_REPORT.json`
13. Uninstaller removes only a PAK containing the exact Final V2 marker and stops on ambiguous multiple-marker states.

## Static verification

Built-in synthetic self-test result:

`SELFTEST PASS: 137 families, 32 NORMAL/PERMA broad pools, family-equalized category shares`

Synthetic coverage includes:
- 137 unique families
- 15 rank bundles per family
- 9 current-style paired rarity/source pools
- all 16 infected
- NORMAL + PERMA for all 16 = 32 route rebuilds
- broad family coverage in every generated selector
- merged original paired routes with redundant calls zeroed

## Runtime status after release

Final V2 itself remains runtime TEST-PENDING until user installs it and confirms:
- weapon rotation is materially broader than proof subset;
- each dropped weapon still arrives with matching blueprint;
- resource/charm/Night Sovereign behavior remains intact;
- corpse interaction / stash / current weapon identity remain normal;
- optional save/reload blueprint persistence check.

## Next work after Final V2 GREEN

Once broad global weapon+blueprint loot is GREEN, stop changing loot architecture. Future additions must reuse the same global `tbp_*` layer together with the proven resource/high-loot system.

Then proceed separately to:
- Exotic blueprint tier research
- Iconic blueprint tier research
- Legend 1–300 / post-level-15 progression research

without reopening the rejected local loot route.
