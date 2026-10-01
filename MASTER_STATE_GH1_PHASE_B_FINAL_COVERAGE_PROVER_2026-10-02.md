# GH1 Phase B — Runtime Proof + Final Coverage Prover — 2026-10-02

## Runtime evidence now received

Broad Global Final V2 is runtime-active and materially broader than the generated-only proof subset.

User-observed Broad Final V2 weapon+blueprint pairs include:
- Collector's Piece
- Butcher's Dream
- Fireman's Bane
- Medieval Mace
- Leather Hammer
- In Jade's Memory
- Simple Machete
- Survivalist SMG
- plus additional varied weapons.

All observed examples arrived together with their matching blueprint.

Combined with the earlier generated-only proof (K13, .38 Revolver, Steel Bat, Tonfa, C15 Rifle, Skull Cracker, Sunray, The Elite), the following are locked:
- GLOBAL `tbp_*` loot route: RUNTIME PROVEN.
- weapon + matching blueprint bundle delivery: RUNTIME PROVEN.
- clean-room generated blueprint acquisition path: RUNTIME PROVEN.
- Broad Final V2 variety improvement: RUNTIME PROVEN.

Save/reload persistence remains separately runtime-confirmable unless explicitly reported.

## Native vs generated classification rule

Do not classify from public display-name databases or community blueprint lists.

Canonical project classification is data-driven:
- NATIVE = the weapon family already has a Weapon craftplan in official `data0/data1` `collectables_ft.scr`.
- GENERATED = the family has a current GH1 weapon craftplan but is absent from official `data0/data1` weapon craftplans.

This exact official-vs-current comparison is also the rule used by the generated-only proof.

## Final mechanical proof tool

Artifact:
`GH1_PHASE_B_FINAL_COVERAGE_PROVER_V1.zip`

SHA256:
`80918722a61fab4dcd3c98f438435ab4beef435fa2c0163ad607d2987fab176f`

Core source:
`tools/tbp_phase_b_final_coverage_prover.py`

Core SHA256:
`aebf57bcb51ef688dc4217bde3153ef5e866abb8de4810a245ad2d4c7c3cf77e`

The prover is READ-ONLY. It does not install, overwrite, delete or patch PAKs.

It validates the live installed Broad Final V2 stack and requires all of the following for `PHASE_B_DATA_PROVEN`:
1. exactly one Broad Final V2 marker PAK;
2. exact project family universe = 137 weapon families;
3. all 137 families have weapon+matching-blueprint pair bundles;
4. every family is reachable from the original paired source pools retained under Final V2;
5. every infected NORMAL/PERMA section has exactly one active BroadV2 selector;
6. original paired source calls are zeroed in Final V2;
7. every BroadV2 selector contains exactly the same source pair-bundle universe for its section;
8. every section has 137/137 family coverage;
9. all 16 infected x NORMAL/PERMA = 32/32 route sections;
10. no unreachable family remains.

Outputs:
- `Documents\GH1_PHASE_B_FINAL_COVERAGE_PROOF_V1.json`
- `Documents\GH1_PHASE_B_FINAL_COVERAGE_FAMILIES_V1.csv`

The CSV explicitly lists each internal family, native/generated classification, kind, blueprint ID, rank count/ranks and reachability.

## Static test completed

Self-test:
`SELFTEST PASS: 137 families, native/generated classification, exact bundle identity, 32 broad selectors`

Full synthetic live-stack audit also passed:
- status `PHASE_B_DATA_PROVEN`
- 137/137 pair families
- 137/137 reachable families
- 32/32 route sections
- exact source/broad pair-universe equality

## Final lock condition

Once the prover is run against the user's actual installed Broad Final V2 stack and returns:
- `STATUS: PHASE_B_DATA_PROVEN`
- `All pair families: 137 / 137`
- `Reachable families: 137 / 137`
- `Route sections: 32 / 32`

then lock Phase B global weapon+blueprint coverage as DATA PROVEN and stop modifying the loot architecture.

Future weapon/resource loot additions must continue through the same global `tbp_*` layer.
