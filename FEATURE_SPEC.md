# FEATURE SPECIFICATION

## 1. Universal Legendary eligibility

All supported weapons may generate as native Legendary even when their vanilla rarity ceiling is Rare or Epic. The implementation must alter the actual generated item quality/state where the engine permits it.

## 2. Global rarity gacha

Every generated weapon from supported loot sources participates in a rarity roll. Initial Legendary target: **30% per generated weapon**.

## 3. Common infected weapon availability

Increase the chance that low-tier infected generate/drop weapons modestly. Initial Biter target: **20–25% weapon availability**, subject to actual vanilla loot semantics.

## 4. Human held-weapon drops

Humans may drop the weapon they are visibly carrying. That exact weapon participates in the same rarity roll and may become Legendary. Initial held-weapon drop target: **60–75%** if technically compatible with vanilla behavior.

## 5. Extra human corpse loot

A small additional corpse weapon roll may exist, but it must remain separate from the held-weapon feature and must not replace it.

## 6. Containers and searchable loot

Supported containers, bags, chests, and other searchable loot sources get moderately increased weapon availability. Generated weapons use the same rarity-gacha rules.

## 7. Destructible loot props

Destructible objects participate only if their actual 1.71E definitions contain loot-generation behavior. Do not fabricate loot for purely visual/destructible props until mapped and deliberately designed.

## 8. Native Legendary properties

Legendary conversion/generation should use real Legendary-compatible quality, affix count/pool, durability/repair behavior, and other relevant native properties where available. Avoid cosmetic-only rarity.

## 9. Legendary persistence

Obtained Legendary state should survive removal of the mod if the game save format persists that state. This is a required validation target, not an assumption.

## 10. Legendary Upgrade Overhaul

Legendary weapons gain stronger upgrade progression than lower rarities. Primary scaling:

- damage: aggressive
- durability: aggressive
- handling/stamina/other supported secondary stats: moderate
- attack speed: conservative

## 11. Legendary Ascension

Per-instance progression:

`L -> L+1 -> L+2 -> L+3 -> L+4 -> L+5`

Initial cumulative target envelope, subject to engine constraints and balance testing:

| Stage | Damage | Durability | Secondary stats | Attack-speed ceiling target |
|---|---:|---:|---:|---:|
| L | native | native | native | native |
| L+1 | +12% | +15% | small | ~+2% |
| L+2 | +25% | +32% | moderate | ~+4% |
| L+3 | +40% | +50% | moderate | ~+6% |
| L+4 | +60% | +72% | high | ~+8% |
| L+5 | +85% | +100% | highest | ~+10% |

These numbers are tuning targets, not frozen until in-game testing confirms safe behavior.

## 12. Legendary Core

Add a progression item/mechanism named **Legendary Core** unless 1.71E technical constraints require a safe alternate implementation.

Behavior:

- Rare/Epic + 1 Core -> Legendary
- Legendary + Core(s) -> next Ascension stage

## 13. Core drop chances

Initial targets:

| Source | Core chance target |
|---|---:|
| Common infected | 8–10% |
| Viral | ~10% |
| Human | ~10% |
| Ordinary container | 8–10% |
| Special infected | 12–15% |
| Good/locked chest | 12–15% |
| Boss/Chimera | 20–30% |

## 14. Core costs

| Transition | Cost |
|---|---:|
| Rare/Epic -> Legendary | 1 |
| L -> L+1 | 1 |
| L+1 -> L+2 | 2 |
| L+2 -> L+3 | 3 |
| L+3 -> L+4 | 5 |
| L+4 -> L+5 | 8 |

## 15. Per-weapon state

Two copies of the same weapon definition may have different progression states. Example:

- Katana A: Legendary L+0
- Katana B: Legendary L+4

A global definition-only buff does not satisfy this requirement unless the engine provides no persistent per-instance path; any such limitation must be documented.

## 16. Preserve weapon identity

Do not unnecessarily change weapon model, base name, animation class, or category. The mod extends rarity, loot, stats, and progression rather than replacing weapon identity.

## 17. Preserve RNG

The system intentionally makes good weapons easier to obtain but does not guarantee Legendary every time. Farming and random outcomes remain part of the loop.

## 18. Balance is config-driven

All tunable probabilities, Core costs, and Ascension target multipliers should live in project-authored configuration wherever practical so balance changes do not require rewriting patch logic.
