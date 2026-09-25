# GLOBAL LOOT ROOT V1 — runtime result

Status: **RUNTIME-PROVEN for scene changes and save-data swaps**.

User runtime report on 2026-09-26:

- before GLOBAL ROOT V1, custom loot worked during the Safe Haven tutorial but reverted to vanilla after the tutorial finished / co-op became ready / the player left the room and killed newly encountered infected;
- after installing GLOBAL ROOT V1, custom loot remained active across repeated scene changes;
- custom loot also remained active after changing/replacing save data;
- user described GLOBAL ROOT V1 as working perfectly for this persistence problem.

Therefore the mod-owned root binding architecture is accepted as runtime-proven for the two failure modes that were actually reproduced:

1. scene / level transitions;
2. save-data swaps / replacement.

The historical SPECIAL45 payload remains the fallback proven gameplay baseline until later merged features finish testing. GLOBAL ROOT V1 is the proven persistence substrate for future loot-rule work.

Not yet explicitly reported in this runtime result:

- New Game end-to-end persistence;
- NG+ end-to-end persistence.

Do not infer those two cases until tested.

Safety invariants remain:

- preserve `LootedObject` topology;
- do not embed loot definitions into saves;
- do not delete/reorder live item definitions;
- do not revive CP1 Alpha4 or Sense V4/V4.1;
- keep loot rules in mod-owned global definitions.
