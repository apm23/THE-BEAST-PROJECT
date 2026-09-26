# REMAKE PROVEN45 — recovered proven G1 transplant specs

These compact project-authored delta specifications were reconstructed from exact historical runtime artifacts recovered from the user's Library.

They do **not** contain complete proprietary game files. Each `.b64` part is compressed JSON containing small old/new context replacements or one custom project block. Runtime builders must apply them to files extracted from the user's owned current DLTB installation.

Recovered exact artifact lineage:

- SPECIAL45 canonical data2: `190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`
- stack 99,999 parent: `77e7ff5630167af4f733bda7e754ab0eb8f90c0491e75403caaeb64077a44155`
- Weapon68 candidate: `8b1587ce0741295e98598a2ea6e22fe67102a6b34644cacd14f7558ea09dde18`
- G1 weapon-access preflight: `6ee08e9d867a9a72b1968b557256747ac701c511f7580b0605f4cd3906e2b5c5`
- G1 Night Sovereign final: `047a44416f7ab8a1bb736cf2aac374a0cb36b96a0ff775ed05ff8ad2e73e4521`

Specs:

- `inventory_ranged.part*.b64` — canonical SPECIAL45 inventory_ranged -> proven G1 preflight weapon/rarity/drop/share state.
- `lootpools_g1.part*.b64` — canonical SPECIAL45 lootpools -> G1 Night Sovereign/Exotic route additions while preserving LootedObject name/order topology.
- `outfits_ft.b64` — vanilla 1.71E outfit carriers -> six Vanguard-based Night Sovereign definitions.
- `itemaffixes.b64` — native affix source -> Night Sovereign armor affix additions.
- `charms.b64` — native charm source -> Night Sovereign Sigil carrier additions.
- `lootsets_append.b64` — project-authored G1 custom sub-pool block to append semantically to the existing current lootsets without importing the old resource-parity parent wholesale.

Apply rule:

1. If the source file matches the captured base SHA, ordinary exact patching is permitted.
2. Otherwise apply only unique context-matched `old -> new` operations.
3. If an `old` block is absent and the corresponding `new` block is not already present, stop. Never guess.
4. Never delete/reorder `LootedObject(...)` definitions.
5. Never use these specs to revive Global Loot Root V1, Sense wallhack, CO-OP routing, save-versioning, or stash rewrites.

The 1.71PE final package remains `CANDIDATE_NOT_RUNTIME_GREEN` until in-game hard gates pass.