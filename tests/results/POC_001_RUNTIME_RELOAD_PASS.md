# POC-001 runtime + reload result

Date: 2026-09-20
Target: Dying Light: The Beast VER. 1.71E
POC: Native Legendary Opportunity/Camp Axe

## Result

PASS for runtime identity and save/reload with POC still installed.

Observed in user screenshots after quitting the game and launching again:

- Display name: `CAMP AXE`
- Rarity/type: `LEGENDARY ONE-HANDED AXE`
- Damage: 131 Slashing / 131 Base Damage
- Affixes remained present:
  - +33% Damage (Melee Weapon Throw)
  - +6% Damage (Infected)
  - -7.5% Stamina Cost (Melee Weapons)
- Durability remained `160/160`
- Repairs remaining remained `7/7`
- Modify UI still exposed four sockets:
  - Tip Socket
  - Shaft Socket
  - Grip Socket
  - Charm Socket

This confirms the POC item survives a normal save/quit/relaunch cycle while `data2.pak` remains installed. It does NOT yet prove persistence after POC removal.

## Next safe action

1. Close the game.
2. Back up the current modified test save.
3. Remove only the exact POC-001 `data2.pak` using the checksum-safe uninstaller.
4. Launch the game without the POC.
5. Re-open the same save and inspect the same Camp Axe.
6. Record whether rarity, affixes, durability/repairs, and sockets persist or are recomputed from vanilla definitions.

Do not proceed to global rarity gacha, Legendary Core, or Ascension until this uninstall-persistence result is known.
