# REMAKE 1.71PE MASTER STATE

Branch authority: `remake-proven45`.

Continuity: `BEAST-PROVEN-SWITCH45`.

This document is authoritative for the current remake branch together with actual branch HEAD. Historical `MASTER_STATE.md` remains preserved as lineage/history and must not be rewritten to erase proven results.

## Current runtime target

- Game: Dying Light: The Beast
- Current runtime target: **1.71PE**
- Historical captured baseline: **1.71E**
- Behavioral foundation: **USER HIGH LOOT SPECIAL45 / PROVEN45**
- Canonical historical SPECIAL45 data2 SHA-256: `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

1.71PE must be extracted and compared against the captured 1.71E target set before any gameplay candidate is built. If any of the three canonical SPECIAL45 core inputs differ, a dedicated port must be authored rather than applying the 1.71E delta blindly.

## Immutable foundation

PROVEN45 is the loot foundation. Do not replace it with GLOBAL ROOT V1 or another global-root architecture in this remake.

Frozen invariants:

- preserve `LootedObject` topology and corpse routing;
- corpse loot `F` is a hard gate;
- no save-versioning rewrite;
- no stash-DLC rewrite;
- no `player_variables` rewrite;
- no invented quickslot SLOT5-SLOT8 behavior;
- no aggressive root replacement;
- no silent held-weapon-drop feature;
- no Legendary Core / Ascension system.

## Current single-player core scope

1. PROVEN45 loot behavior preserved.
2. Native weapon rarity extended through **Exotic** where engine-native definitions support it; no cosmetic-only rarity.
3. Human enemies receive zombie-style **corpse/search lootpool** behavior; their visibly held weapon is not the project feature.
4. Special infected receive controlled high-tier / Exotic opportunities using existing native mechanisms and RNG.
5. Rebuild the custom powerful outfit without touching frozen loot topology or save/versioning.
6. Inventory targets: Equipment 34, Consumable 34, Weapon 68, Ammo 42.
7. Material / consumable / throwable stack target: 99,999 where the current-runtime definitions safely expose stack limits.
8. Dismantle compatibility must remain functional.
9. Drop/share compatibility must remain functional.
10. Save reload, save swap, and scene transition are required gates.
11. Attack / controls remain normal.

## Deferred

Not part of the current core build:

- Sense wallhack;
- dormant/dead Sense logic;
- one-sided CO-OP;
- CO-OP data2-only switch work.

Historical one-sided CO-OP success remains recorded and may be reintroduced after the single-player core is runtime-green.

## Cancelled for this remake

- Legendary Core;
- Legendary Ascension;
- L+1..L+5;
- Core drop/cost system;
- human held-weapon drop as a project feature;
- Manual Save Anywhere.

## Current tooling pipeline

Primary prep entry point:

`tools\RUN_1.71PE_CORE_PREP.cmd`

It performs current-install extraction, compatibility comparison, port-plan generation, CURRENT_RUNTIME preparation, and current-runtime mapping collection for rarity/human/special-infected/outfit/inventory/stack work.

Compatibility outputs:

- `local_build/COMPAT_1.71PE_VS_1.71E/compatibility.json`
- `local_build/COMPAT_1.71PE_VS_1.71E/compatibility.txt`
- `local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.json`
- `local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.txt`

Mapping outputs are local-only and intentionally not committed because they derive from the user's owned game files.

## Build discipline

Every gameplay builder must:

1. verify its source baseline / expected hashes;
2. fail closed on unknown anchors or multiple ambiguous anchors;
3. whitelist changed files;
4. preserve untouched files byte-exact;
5. produce a build manifest with source hashes and output hash;
6. mark output `CANDIDATE_NOT_RUNTIME_GREEN` until user runtime testing passes;
7. keep rollback possible to the canonical PROVEN45 path.

## Runtime test order

For every combined candidate:

1. boot game;
2. confirm attack/control input;
3. confirm corpse `F` interaction;
4. inspect ordinary infected loot;
5. inspect human corpse loot;
6. inspect special infected loot;
7. verify Rare/Epic/Legendary/Exotic behavior actually represents native state, not only color/text;
8. verify custom outfit and its intended effects;
9. verify inventory capacities;
10. verify stack limits;
11. dismantle relevant items;
12. drop/share where applicable in the current single-player test context;
13. save -> exit -> reload;
14. change scene/level -> repeat corpse/loot/inventory checks;
15. swap a test save -> repeat checks.

Any regression in `F`, attack/control, save integrity, DLC behavior, or scene persistence rejects the candidate immediately.

## Runtime status

Repository/tooling preparation can be completed without proprietary game bytes. The final 1.71PE gameplay PAK cannot honestly be marked finished or runtime-green until the local 1.71PE extraction/mapping is run and the resulting candidate is tested in game.

Do not infer New Game or NG+ persistence until explicitly tested.