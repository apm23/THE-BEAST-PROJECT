# GH1 Phase B — Generated-Only Global Proof V2 — 2026-10-02

## Runtime evidence received

Global V1 is confirmed to produce weapon + blueprint loot in runtime, but the user reports poor variety / only a small subset appearing. This does **not** yet prove the clean-room generated blueprint path, because the observed pairs may all be weapon families that already have Techland/native blueprints.

Therefore:
- Global `tbp_*` routing is runtime-active.
- Weapon+blueprint output exists.
- Generated-blueprint path remains **TEST-PENDING**.
- Do not claim Phase B generated blueprints GREEN yet.

## Locked architectural rule

All future zombie weapon/resource loot work stays in the proven GLOBAL GH1 layer:

`default.loot -> tbp_lootpools_global_v1.loot -> tbp_lootsets_global_v1.loot`

Do not return to the rejected isolated/local vanilla loot route. Do not mass-edit weapon definitions or `LinkedItems`.

## Generated-only proof strategy

Artifact:
`GH1_PHASE_B_GENERATED_ONLY_GLOBAL_PROOF_V2.zip`

Package SHA256:
`4b61a53d63de3fa442fcb16666852093c4feab5b098ab1879b264aa32a576f7c`

The proof installer is dynamic and operates only on the user's already-installed Global V1 stack:

1. Resolve the effective live version of:
   - `scripts/inventory/collectables_ft.scr`
   - `scripts/inventory/loot/tbp_lootpools_global_v1.loot`
   - `scripts/inventory/loot/tbp_lootsets_global_v1.loot`
   from the highest `dataN.pak` containing each file independently.
2. Read official `data0/data1` `collectables_ft.scr` as the native blueprint reference.
3. Parse all weapon craftplans by `CraftplanType("Weapon")` + `ScaleWithPlayerRank(...)`.
4. Define a generated family as a T1 weapon blueprint family present in current Global V1 collectables but absent from official data0/data1.
5. Find current Global V1 `ItemBundle` pairs containing:
   - exact weapon rank `<family>rN`
   - matching generated T1 blueprint.
6. Discover the current global paired lootset subs that actually reference those bundles.
7. Separately discover **all** current weapon+blueprint pair pools, native and generated, so native routes can be suppressed during proof.
8. Build a temporary `TBP_PhaseB_GeneratedOnlyProof` sub, using up to 6 firearm + 6 melee generated families while preserving `PlayerLevelRestriction(rank, rank)`.
9. In the existing 16 global infected `LootedObject` blocks, preserve topology but temporarily:
   - replace the first paired weapon route in each NORMAL/PERMA section with `TBP_PhaseB_GeneratedOnlyProof`, test weight `50.0`;
   - set other normal weapon+blueprint pair-pool weights to `0.0` for proof purity.
10. Write a NEW highest-number `dataN.pak` overlay. Existing PAKs are not overwritten.
11. Attempt save backup and write:
   `Documents\GH1_PHASE_B_GENERATED_ONLY_PROOF_V2_REPORT.json`
12. Uninstaller deletes only a PAK containing the exact V2 marker and refuses ambiguous states.

## Why this proof is decisive

The proof does not invent a separate fake blueprint. It selects blueprint definitions that are already part of Global V1 but verifies they are absent from official data0/data1. If one selected weapon+blueprint pair drops during this proof and the blueprint persists through save/reload, the generated path is proven independently from Techland/native blueprint families.

## Static verification completed before release

- Parser/patcher self-test: PASS.
- End-to-end synthetic split-stack test: PASS.
- Tested layout: official `data0`, global loot files in `data2`, generated collectables in `data3`, unrelated project/mod layer in `data4`.
- Proof created fresh `data5.pak` overlay.
- 16 infected x NORMAL/PERMA = 32 generated-only proof routes confirmed.
- Marker/report generation confirmed.
- Safe uninstaller removed only proof `data5.pak`.

## Runtime test requested

1. Close game.
2. Run `1_INSTALL_GENERATED_ONLY_PROOF.cmd`.
3. Start game and kill infected normally; proof route weight is deliberately high.
4. When the first weapon+blueprint pair appears, compare it to `selected_pairs` in the generated report.
5. Confirm blueprint is visible/usable.
6. Save, reload, confirm it remains.
7. Close game and run `2_UNINSTALL_PROOF.cmd`.

## Next action after runtime result

If generated-only proof is GREEN:
- stop test forcing;
- keep generated pair mechanism;
- rebuild the final GLOBAL weapon pool for broad family variety and sane balance;
- merge that final global weapon pool with the proven resource/high-loot global layer as requested by the user;
- then proceed to later Exotic/Iconic + Legend progression research without changing the loot architecture.

If generated-only proof reports zero generated families / zero reachable generated bundles, or only native pairs remain:
- treat Global V1 generator/reachability as FAIL;
- rebuild generated blueprint definitions/pair-pool reachability before any final loot balancing.
