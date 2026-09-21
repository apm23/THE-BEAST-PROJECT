# POC-003 runtime uninstall result

Target: Dying Light: The Beast **1.71E**

POC: `POC_003_L1_CARRIER`

## Runtime sequence

A newly generated controlled Legendary Camp Axe was inspected before reload, after a full save/quit/reload with POC-003 still installed, and again after uninstalling POC-003 and loading the same save in vanilla 1.71E.

### POC-003 active — initial inspection

- item: Camp Axe
- rarity: Legendary One-Handed Axe
- displayed/base damage: **147**
- visible affixes:
  - `+6% Damage (Infected)`
  - `+20% Damage (Accessories)`
  - `-7.5% Stamina Cost (Melee Weapons)`
- durability: **160/188**
- repairs: **7/7**
- native carrier shown in UI: **Spark — Applies SHOCK on critical hits**
- Shaft / Grip / Charm sockets visible in addition to the occupied Tip carrier

### Save -> quit -> reload with POC-003 still installed

**PASS.**

The same item still showed:

- damage **147**
- durability **160/188**
- repairs **7/7**
- same listed affixes
- Spark / SHOCK still visible

No POC-specific stat drift was observed while the POC definition remained loaded.

### After POC-003 uninstall -> vanilla reload

Observed on the same saved weapon:

- rarity remained Legendary
- listed affixes remained the same
- damage changed **147 -> 142**
- max durability changed **188 -> 185** while current durability remained **160**
- repairs remained **7/7**
- Tip/Shaft/Grip UI disappeared; only vanilla Charm Socket remained
- Spark text/UI was no longer exposed because the POC-added socket structure disappeared
- the Shock hardware/visual attachment still appeared physically attached to the axe in the supplied runtime screenshot
- post-uninstall SHOCK combat-proc functionality was not tested in this comparison and must not be claimed from the screenshot alone

## Interpretation

**POC-003 is NOT a strong persistence pass.**

The deliberately non-vanilla POC-003 stat signature did not survive removal of the defining POC. The weapon remained valid and persistent, but its damage/max-durability values changed on clean vanilla reload.

This rejects the specific strategy of using a native installed-mod identity plus temporary global CraftPart parameter overrides as an arbitrary persistent Ascension-stat carrier. The carrier/mod attachment can persist strongly, but the custom modifier magnitude is still definition-dependent rather than proven serialized per item.

The result is compatible with the POC-003 `Partial pass` branch, except that post-uninstall SHOCK functionality has not yet been directly combat-tested. Regardless of that remaining carrier-function detail, the POC-specific L+1 stat-signature goal already failed.

## Frozen consequence

- Preserve POC-001 and POC-002 as frozen green.
- Do not extend this POC-003 parameter-override strategy to L+2..L+5.
- Do not claim custom per-item Ascension values survive uninstall through this mechanism.
- Next weapon research must identify a different serialized per-item field/state or another native carrier whose magnitude itself is stored on the weapon instance.