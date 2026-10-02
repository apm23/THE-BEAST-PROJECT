# GH1 Phase B — Final Data Proven — 2026-10-02

## User runtime result

Broad Global Final V2 produced broad weapon variety in normal play, including examples such as Collector Piece, Butcher's Dream, Fireman's Bane, Medieval Mace, Leather Hammer, In Jade's Memory, Simple Machete, Survivalist SMG, and others. Each observed weapon arrived together with its matching blueprint.

This confirms the Broad Final V2 runtime selector is materially broader than the earlier generated-only proof subset.

## Generated blueprint runtime proof

Generated-only Global Proof V2 previously selected only weapon families whose T1 weapon blueprint was absent from official data0/data1 collectables and present only in the GH1 current collectables layer. Runtime produced repeated weapon + matching blueprint packages from that generated-only selector.

Therefore:
- generated blueprint acquisition through loot is runtime PROVEN;
- weapon + matching-blueprint bundle delivery is runtime PROVEN.

## Final live coverage audit

User first ran GH1_PHASE_B_FINAL_COVERAGE_PROVER_V1 against the live Broad Final V2 stack.

V1 live scan facts:
- all paired weapon families: 137
- native families: 49
- generated families: 88
- total defined pair bundles: 2041
- legacy/source route families: 126
- legacy/source pair bundles: 1876
- Broad Final route sections: 32
- every Broad selector reported 137 families
- every Broad selector reported 2041 recognized pair bundles
- every Broad selector outer weight was positive
- the legacy/source route was a subset of Broad Final
- Broad Final added 165 recognized pair bundles = 11 families x 15 ranks

## V1 prover false negative

Coverage Prover V1 reported PHASE_B_DATA_NOT_PROVEN because it incorrectly required the legacy source bundle universe and the Broad Final bundle universe to be identical.

That requirement was wrong for the intended architecture.

Broad Final V2 deliberately promotes 11 families that were missing from the legacy source routes. The 165 "extra" pair bundles are therefore desired coverage, not unknown/error content.

The 11 promoted source-gap families are:
- dlc_ft_firearm_flamethrower_r — native
- dlc_ft_firearm_grenadelauncher_r — native
- dlc_ft_firearm_pistol_b_legendary_r — generated
- dlc_ft_firearm_revolver_1stanniversary_r — native
- dlc_ft_firearm_revolver_c_legendary_r — generated
- dlc_ft_firearm_rifle_1stanniversary_r — native
- dlc_ft_firearm_rifle_a_legendary_r — generated
- dlc_ft_firearm_sawbladelauncher_r — native
- dlc_ft_firearm_shotgun_1stanniversary_r — native
- dlc_ft_firearm_shotgun_b_legendary_r — generated
- dlc_ft_firearm_smg_e_legendary_r — generated

## Corrected proof rule

A Broad Final selector is complete when:
1. all 137 defined paired weapon families exist;
2. its recognized pair-bundle set equals the complete current pair universe;
3. all 32 infected NORMAL/PERMA sections have exactly one positive Broad selector;
4. old paired source routes remain zeroed;
5. no defined pair family is missing from the Broad selector.

## Corrected artifact

GH1_PHASE_B_FINAL_COVERAGE_PROVER_V2.zip

Package SHA256:
e28ca5ab296aa4fa82956e07224ccd995fdb3a71e210effef8e20c95550f5ff8

V2 fixes the reachability definition:
- source route coverage is informational baseline only;
- reachability is measured from the active Broad Final selectors;
- every Broad selector is compared against the complete current all-pair universe rather than the legacy source universe.

Synthetic self-test:
PASS — legacy source 126 families -> every Broad selector promotes exact complete 137-family / all-pair universe.

## Actual Prover V2 live rerun — PASS

User reran GH1_PHASE_B_FINAL_COVERAGE_PROVER_V2 on 2026-10-02 against the installed Broad Final V2 stack.

Actual report status:
PHASE_B_DATA_PROVEN

Verified live:
- expected family count: 137
- all pair family count: 137
- reachable family count: 137
- native family count: 49
- generated family count: 88
- pair bundle count: 2041
- broad bundle count: 2041
- infected block count: 16
- route section count: 32
- unreachable families: 0
- issues: 0
- every one of the 32 Broad route sections contains all 137 families
- every one of the 32 Broad route sections contains all 2041 recognized pair bundles
- every route has zero missing all-pair bundles
- every route has zero unknown Broad bundles
- every route has a positive Broad weight
- every route carries the intended 165 promoted source-gap bundles

Rank-domain audit from the V2 CSV:
- 137 family rows total
- all 137 rows reachable=true
- 136 families define ranks 1 through 15
- dlc_ft_wpn_1hs_knife_p_preorder_r legitimately defines only rank 15
- therefore the complete valid pair universe is exactly 136*15 + 1 = 2041 bundles
- there is no missing rank/bundle gap in the defined family universe

This actual V2 rerun supersedes the earlier V1 false-negative interpretation.

## Locked Phase B status

FINAL PROVEN:
- global tbp_* loot architecture runtime-active
- generated-blueprint acquisition
- weapon + matching blueprint pairing
- broad runtime variety
- 137/137 paired weapon-family Broad coverage
- complete 2041/2041 valid pair-bundle Broad coverage
- 32/32 NORMAL/PERMA Broad route coverage
- zero unreachable families
- zero unknown Broad bundles
- zero coverage issues

Do not reopen the rejected local loot architecture.

Future weapon loot additions must reuse the same global tbp_* layer.

Blueprint save/reload persistence remains a separate runtime persistence assertion unless explicitly confirmed by the user; it does not affect the Phase B family/bundle/route coverage proof.
