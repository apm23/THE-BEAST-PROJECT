# MASTER_STATE

## Authority

This file plus the actual GitHub HEAD are the source of truth for project continuation. Reconcile both before making changes. Do not reconstruct state from chat memory when repository state disagrees.

## Current baseline

- Game: **Dying Light: The Beast**
- Target build observed in-game: **VER. 1.71E**
- Installation state at baseline: **fresh install, no mods installed**
- Clean test save captured: `save_ft_0.sav`
- Clean test save SHA-256: `82af1723995ab086853934f67551b7ac61e2f7587191a4952d6e04c3e15ee4d5`
- Save file itself must remain local/private and must not be committed.

## Current phase

**PHASE 0B — bootstrap complete; clean vanilla mapping next**

No gameplay patch has been shipped yet.

## Frozen project goals

1. Universal native Legendary eligibility for weapons even when vanilla caps them at Rare/Epic.
2. Global per-weapon rarity gacha, target initial Legendary roll ~30% when a weapon instance is generated.
3. Slightly increased weapon availability from common infected, humans, searchable/destructible loot sources that actually own loot definitions.
4. Human held-weapon drop participates in the same rarity roll; the actual weapon being carried may become Legendary.
5. Legendary rarity should be a real item state/quality, not merely cosmetic text/color.
6. Legendary Core item/progression mechanic.
7. Rare/Epic + Core -> native Legendary when technically possible.
8. Legendary + Core -> per-item Legendary Ascension progression L+1 through L+5.
9. Ascension emphasizes damage and durability; secondary stats increase more conservatively; attack-speed changes must stay animation/hit-registration safe.
10. Progression should be per weapon instance, not a global buff for every weapon of the same definition.
11. Persistence is a hard requirement to investigate and test: obtained Legendary/Ascension state should survive mod removal wherever the engine/save format permits.
12. Keep RNG/farming; do not force every drop to Legendary.

## Initial balance targets

- Legendary chance per generated weapon: **30%** initial target.
- Common Biter weapon availability target: approximately **20–25%**, subject to actual vanilla loot semantics.
- Human held-weapon drop target: approximately **60–75%**, subject to actual drop implementation.
- Legendary Core target chances:
  - common infected: 8–10%
  - Viral/human: ~10%
  - special infected: 12–15%
  - ordinary containers: 8–10%
  - good/locked chest: 12–15%
  - boss/Chimera: 20–30%
- Core costs:
  - Rare/Epic -> Legendary: 1
  - Legendary -> L+1: 1
  - L+1 -> L+2: 2
  - L+2 -> L+3: 3
  - L+3 -> L+4: 5
  - L+4 -> L+5: 8

## Technical invariants

- Do not commit original `data*.pak`, extracted vanilla archives, save files, or other copyrighted game dumps.
- Prefer patch/config/build tooling over redistributing vanilla content.
- Never claim persistence until uninstall/reload testing proves it.
- Never fake Universal Legendary by only recoloring/relabeling lower rarity.
- Do not globally overwrite all copies of a weapon when a per-instance upgrade path is technically available.
- Treat attack speed separately from damage/handling because excessive animation speed may break hit behavior.

## Confirmed artifacts

- Repository created and accessible: `apm23/THE-BEAST-PROJECT`.
- `README.md` defines baseline and authority order.
- `PROJECT_CONTRACT.md` freezes non-negotiable behavior and continuation protocol.
- `FEATURE_SPEC.md` records the agreed feature set and initial tuning envelope.
- `TEST_MATRIX.md` defines proof-of-concept, statistical, integrity, and uninstall/persistence tests.
- `config/balance.json` contains project-authored initial probabilities, Core costs, and Ascension targets.
- `tools/validate.py` statically validates probability/config bounds.
- `.github/workflows/validate.yml` is present for GitHub Actions validation; no workflow run has been observed yet.
- `tools/collect_baseline.ps1` can locally enumerate relevant paths from `data*.pak` without committing game archives.
- `.gitignore` blocks PAKs, saves, extracted baselines, and local baseline output.
- Clean baseline screenshot shows `VER. 1.71E`.
- Clean save archive supplied for local testing/reference; one save file exists inside.

## Unknowns to resolve before gameplay patching

1. Exact 1.71E paths and schemas for weapon definitions, rarity caps, loot tables, item affixes, blueprint/upgrade rules, and persistent per-item attributes.
2. Whether rarity is persisted directly on each item instance or recomputed from its definition on load for every relevant weapon family.
3. Whether an unused/native persistent field can safely encode Ascension level.
4. Whether Legendary Core can be implemented as a genuinely new inventory item or should reuse a safe existing item/category with a custom recipe/action.
5. Which destructible props actually own loot tables versus visual-only destruction.
6. Exact semantics of human held-weapon generation/drop and when rarity/quality is assigned.

## Failed hypotheses

None yet. Do not add speculative failures; record only tested/reproduced failures.

## Frozen-green systems

None yet. A system becomes frozen-green only after validator + in-game tests pass and the evidence is recorded.

## next_safe_action

**Map the clean 1.71E vanilla data before altering gameplay.**

Run `tools/collect_baseline.ps1` against the clean local game install to generate `local_baseline/relevant_file_list.txt` and `baseline_summary.txt`, then inspect only the relevant paths for:

- weapon inventory definitions
- rarity/quality definitions
- affixes
- loot tables for Biters/Virals/humans/containers
- blueprint/crafting/upgrade definitions
- item persistence/saveable attributes

After exact 1.71E paths are confirmed, document them here and add the smallest patch for one controlled proof-of-concept weapon/loot source before attempting the full system.
