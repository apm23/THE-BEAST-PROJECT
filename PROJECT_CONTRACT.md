# PROJECT CONTRACT

## Purpose

Build a mod for **Dying Light: The Beast VER. 1.71E** centered on universal Legendary weapon eligibility, faster but still random weapon farming, and per-weapon Legendary Ascension.

## Non-negotiable behavior

### Native rarity, not cosmetics

A weapon that is normally capped below Legendary should be able to exist as a genuine Legendary item instance when technically possible. A solution that only changes display color/name is not acceptable.

### Global rarity gacha

When a weapon instance is generated from eligible sources, it should participate in the same rarity roll regardless of whether it came from a common infected, a human, a container, or another supported loot source. Initial target: ~30% Legendary per generated weapon.

### Human held weapons

The actual weapon carried by a human can drop and must participate in the rarity roll. The feature must not be limited to an unrelated extra corpse-loot weapon.

### Slightly faster farming

Increase weapon availability from low-value/common sources moderately, not to guaranteed drops. Preserve farming/RNG rather than flooding inventory.

### Legendary Core

Provide an item/progression mechanism with two roles:

- Rare/Epic weapon + Core -> Legendary.
- Legendary weapon + Core -> further per-item Ascension.

The initial Core availability target is roughly 10% from common sources, with modest bonuses for higher-tier encounters/chests.

### Per-item Ascension

Legendary Ascension is individual to the weapon instance:

`Legendary -> L+1 -> L+2 -> L+3 -> L+4 -> L+5`

Damage and durability are the primary scaling axes. Secondary stats may increase. Attack speed must remain conservative and safe for animation/hit registration.

### Persistence-first design

Prefer values that are stored on the item/save over runtime-only global multipliers. Persistence claims require an explicit test:

`obtain/upgrade -> save -> exit -> remove mod -> reload -> inspect item`

If an effect cannot persist without the mod because the engine stores it only in a global definition, document that limitation rather than presenting it as permanent.

## Scope discipline

- Preserve weapon model, identity, animation class, and core gameplay behavior unless a specific feature requires otherwise.
- Do not make all weapons Legendary by default.
- Do not use a blanket global damage cheat as a substitute for per-weapon progression.
- Do not silently alter unrelated game systems.
- Use the smallest patch that proves each technical assumption before expanding globally.

## Repository rules

Allowed in this public repository:

- project-authored configs
- patch descriptions/diffs
- scripts and validators
- workflow files
- documentation
- test records
- hashes/metadata for locally owned baseline files

Do not commit:

- original game archives
- extracted full vanilla data dumps
- save files
- account/user identifiers
- copyrighted game assets not authored by this project

## Continuation protocol

Before any new work:

1. Inspect actual GitHub HEAD.
2. Read `MASTER_STATE.md` completely.
3. Read this contract.
4. Inspect only the files/tests relevant to `next_safe_action`.
5. Preserve frozen-green systems and documented failed hypotheses.
6. Perform the smallest justified next action.
7. Update `MASTER_STATE.md` after meaningful state changes.
