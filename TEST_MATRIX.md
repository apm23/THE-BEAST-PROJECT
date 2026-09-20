# TEST MATRIX

Record every test against an exact commit and game build. Do not mark behavior as confirmed from code inspection alone.

## Baseline

- Target game build: `VER. 1.71E`
- Starting install: clean, no mods
- Clean save available locally

## Required proof-of-concept tests

| ID | Area | Test | Pass condition | Status |
|---|---|---|---|---|
| POC-001 | Load | Install minimal mod package | Game reaches menu and test save loads without crash | NOT RUN |
| POC-002 | Weapon rarity | One controlled normally-capped weapon is generated as Legendary | Inventory reports real Legendary properties, not only recolored text | NOT RUN |
| POC-003 | Persistence | Save POC-002 item, remove mod, reload | Legendary state remains if persisted natively; otherwise limitation is documented | NOT RUN |
| POC-004 | Human held weapon | Kill controlled human with known weapon | The held weapon can drop and its own rarity can roll Legendary | NOT RUN |
| POC-005 | Common infected | Kill controlled Biter sample | Weapon-drop rate changes in intended direction without guaranteed flood | NOT RUN |
| POC-006 | Container | Open controlled common container sample | Weapon availability changes and weapon rarity uses global roll | NOT RUN |
| POC-007 | Core | Obtain/craft Legendary Core | Core exists/works without inventory corruption | NOT RUN |
| POC-008 | Conversion | Use Core on Rare/Epic target | Target becomes genuine Legendary while preserving identity | NOT RUN |
| POC-009 | Ascension | Apply first Ascension to Legendary | Only selected weapon instance receives intended stat increase | NOT RUN |
| POC-010 | Ascension persistence | Save L+1 item, remove mod if technically supported, reload | Persistent state survives or exact dependency is documented | NOT RUN |

## Statistical loot tests

Do not judge probabilities from tiny samples. Initial practical smoke samples may be 30–50 events; balance validation should target at least 200 events per source when feasible.

| ID | Source | Suggested sample | Metrics |
|---|---|---:|---|
| STAT-001 | Common Biter | 200 kills | empty/weapon/non-weapon, rarity counts, Core count |
| STAT-002 | Viral | 200 kills | weapon count, rarity counts, Core count |
| STAT-003 | Human | 200 kills | held drops, bonus weapon drops, rarity counts, Core count |
| STAT-004 | Ordinary containers | 200 opens | weapon count, rarity counts, Core count |
| STAT-005 | Special infected | 100 kills | weapon count, rarity counts, Core count |
| STAT-006 | Good/locked chest | 100 opens | weapon count, rarity counts, Core count |

## Weapon integrity tests

For every weapon family touched by universal rarity:

1. Equip/unequip.
2. Attack repeatedly.
3. Confirm hit registration.
4. Confirm animations are not accelerated beyond safe behavior.
5. Repair if supported.
6. Add/remove normal weapon mods if supported.
7. Store in stash and retrieve.
8. Save/reload.
9. Compare displayed and actual damage behavior.

## Ascension tests

At each level `L+1` through `L+5` record:

- displayed damage
- observed damage where testable
- durability
- handling/stamina-related values
- attack speed/animation behavior
- affixes/mod slots
- repair behavior
- stash round-trip
- save/reload state

## Uninstall/persistence protocol

Use a disposable test save copy.

1. Record weapon identity and all visible stats.
2. Save and exit normally.
3. Back up the save.
4. Remove only this project's mod package.
5. Launch vanilla 1.71E.
6. Load the same test save.
7. Record whether the weapon exists, its rarity, stats, affixes, durability, and Ascension state.
8. Restore backup after destructive/corrupt results.

## Regression gates

A build is not frozen-green if it causes any of the following:

- save cannot load
- inventory corruption
- widespread missing loot unrelated to scope
- held weapons vanish globally
- all loot becomes Legendary unintentionally
- weapon animation/hit detection breaks
- stash round-trip loses upgraded weapon
- probabilities exceed config bounds
- vanilla files are required to be redistributed with the mod
