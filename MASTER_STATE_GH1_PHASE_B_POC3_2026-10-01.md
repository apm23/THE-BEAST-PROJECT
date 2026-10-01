# GH1 Phase B POC3 — Zombie Weapon + Blueprint Pair

Date: 2026-10-01

## Baseline
GH1 Phase A remains GREEN:
- universal weapon dismantle: proven
- universal outfit dismantle: proven
- universal weapon drop: proven
- universal outfit drop: proven

## Rejected / stopped routes
- Phase B POC1 mass LinkedItems inventory override: HARD REJECTED after runtime corruption symptoms (player body/weapon visuals broken, stash weapon identities collapsed, common axe stacking). Rollback restored normal state.
- Phase B POC2 loot-only Viral route: installer STOP AMAN before modifying the game because effective `LootedObject("Viral")` was not found. No runtime state change occurred from that POC.

## New Phase B rule
Blueprint acquisition is now scoped to zombie loot events only.

Desired semantics:
- if a zombie corpse yields a weapon,
- that same corpse loot event also yields/unlocks the matching weapon blueprint,
- normal inventory ownership from stash/trader/other source must not globally trigger blueprint acquisition.

Example user intent: a Goldrush/sniper-class weapon obtained from a zombie should come together with its matching blueprint.

## POC3 architecture
POC3 does NOT patch weapon definitions, `inventory_gen.scr`, `inventory_ranged.scr`, stash/versioning, or global `LinkedItems`.

It resolves the current effective:
- `scripts/inventory/loot/lootpools_ft.loot`
- `scripts/inventory/loot/lootsets_ft.loot`

Then it creates one temporary Biter loot pair using an already-native weapon and its already-native blueprint. The installer lets the user pick a native weapon->blueprint pair whose blueprint is ideally not owned yet.

Test route:
- ordinary Biter corpse
- one temporary high-priority loot branch
- pair sub requests exactly two registered native items from one Set: selected weapon + selected blueprint

Temporary test balance only:
- Biter `LootAmount` is forced to 1 for deterministic validation
- pair branch gets overwhelming weight
- exact Phase A data4 is backed up and restored on uninstall

## Runtime proof required
POC3 is TEST-PENDING until explicit user confirmation of all items below:
1. Biter corpse contains the selected weapon and matching blueprint in the same loot event.
2. Picking them up unlocks/adds the blueprint correctly.
3. Blueprint persists after save/reload.
4. Player body, inventory, stash, weapon identities, Drop, Dismantle, and Sense remain normal.

If only one side of the pair appears, refine loot-pair container semantics. Do not return to the rejected global mass-LinkedItems route.
