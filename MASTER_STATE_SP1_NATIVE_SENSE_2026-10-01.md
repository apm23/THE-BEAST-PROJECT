# SP1 Native Survivor Sense Lock — 2026-10-01

## Authority

This file is a durable addendum to `MASTER_STATE_SP1.md` for the DLTB Sense/ESP branch.

For native Survivor Sense / Biter-through-wall work, this addendum is newer and supersedes the older assumption that custom ESP/W2S is still required for the primary goal.

Continuation code remains: `SP1`.

---

# PRIMARY GOAL — NOW PROVEN BY STATIC NATIVE SENSE CONFIG

Ordinary Biters can be made visible through walls using the game's own native Survivor Sense renderer.

The proven working mechanism is NOT a live memory hook, custom W2S overlay, Biter `.def` assignment, or per-object state transplant.

The proven mechanism is the empty-key hostility fallback in:

`ai/survivor_sense_hostility_presets.scr`

Working block:

```scr
SurvivorSenseHostilityPresets("")
{
    GenericNonHostile("");
    ScriptedNonHostile("");
    GenericHostile("Preset_red_FT");
    ScriptedHostile("Preset_red_FT");
}
```

Runtime result reported by user:

- ordinary Biters are highlighted through walls by native Survivor Sense;
- they appear red like special infected with the initial working mapping;
- resting/sleeping Biters are ALSO highlighted through walls;
- native engine handles occlusion, animation, tracking, and through-wall rendering.

This is the current GREEN / proven route.

---

# Why the fallback works

Earlier runtime N1.3 frozen snapshot proved:

- ordinary Biters are already present in the native Survivor Sense candidate vector;
- Biter `m_XrayEnabled` is already `1`;
- most Biters already pass the early `+0x1060` eligibility state;
- Biter runtime `m_SurvivorSensePreset` is effectively empty/default;
- Viral has a valid tagged runtime Survivor Sense preset handle.

The successful static test demonstrated that empty-preset hostile AI can resolve through a hostility fallback keyed by the empty string.

Therefore the important Biter gate was not candidate registration and not basic XRay enablement. The practical working solution is the hostility resolver fallback for the empty preset key.

---

# DO NOT REPEAT LIVE SENSE HOOK CRASH BRANCHES

The following live experiments caused DLTB force-close and are rejected:

- N1.4 runtime preset-handle transplant;
- N1.5 / N1.5.1 predicate/final-submit CALL wrappers;
- N1.6 transient register preset-handle bridge.

Do not retry these merely to reproduce the working effect. The static config route is simpler and safer.

---

# `.def` findings

The user's uploaded `data3.pak` was audited and 38 closing braces had been swallowed inside `// TBP V5 ALL INFECTED` comments.

Repaired files:

- `humanai_biters.def`: 1 brace;
- `humanai_virals.def`: 2 braces;
- `humanai_infected_special.def`: 1 brace;
- `humanai_dlc_ft_combat.def`: 34 braces.

A repaired `data3.pak` was produced and structurally validated.

However, after repair, direct Biter `.def` Sense assignments still did NOT make Biters visible through walls.

Large-scale 4x Biter-family load-proof tests were also inconclusive/negative enough that `.def` editing is no longer the preferred Sense route.

Keep the repaired `data3.pak` because the syntax cleanup is valid, but do not depend on Biter `.def` edits for Survivor Sense.

---

# Current proven working static artifact lineage

Working baseline artifact:

`DLTB_DATA4_EMPTY_PRESET_HOSTILITY_FALLBACK_READY.zip`

Equivalent clean/minimal lineage:

`DLTB_FINAL_MINIMAL_BITER_SENSE_PATCH.zip`

The important behavior is the empty hostility-key block shown above.

No Lua, DLL patch, camera/W2S, or live memory hook is required for the proven Biter-through-wall function.

---

# Preserved working Sense range state

Current higher-priority player-variable baseline already has:

- `SurvivorSenseRange = 200.0`;
- `SurvivorSenseAIRange = 200.0`;
- `SurvivorSenseRestingAIRange = 200.0`;
- `SurvivorSenseAIHeight = 200.0`;
- `SurvivorSenseAIHeightInterior = 200.0`;
- `SurvivorSenseEnemyBehindPlayerMaxDistance = 200.0`;
- `SurvivorSenseAIDuration = 20.0` before the new V2 tuning;
- `SurvivorSenseSmoothTime = 1.0` before the new V2 tuning.

The 200m resting-AI range is important because the user explicitly confirmed sleeping/resting Biters are highlighted and wants that retained.

---

# Requested enhancement pass — V2

User requested the following on top of the proven working native route:

1. rescan/simplify the working mod without sacrificing functionality;
2. make ordinary Biter highlight cyan / highly visible across outdoor, sewer, and other terrain;
3. minimize the slight highlight fade-in delay for zombies and humans;
4. make far scanned zombies retain XRay longer instead of disappearing quickly after looking away;
5. lock the proven behavior into master state.

Artifact produced for runtime test:

`DLTB_SURVIVOR_SENSE_MASTER_V2_CYAN_INSTANT_PERSIST_READY.zip`

V2 contains only 3 runtime files:

- `ai/survivor_sense_hostility_presets.scr`;
- `ai/survivor_sense_presets.scr`;
- `scripts/player/player_variables.scr`.

V2 design:

- empty-preset hostile fallback -> new dedicated `Preset_biter_cyan_FT`;
- Biter color = electric cyan RGB `0,255,255`;
- Biter day/night alpha = `255/255` for strong visibility;
- `SurvivorSenseSmoothTime`: `1.0 -> 0.03` to make fade-in nearly instant without using literal zero;
- `SurvivorSenseAIDuration`: `20.0 -> 60.0` seconds;
- existing AI Sense presets `MaxVisibilityDistance`: `200 -> 400` meters;
- scan/detection radius remains 200m to avoid doubling scan workload;
- `SurvivorSenseWaveDuration` remains `1.5` so wave behavior itself is not sacrificed;
- sleeping/resting AI detection remains 200m;
- special infected/humans keep their existing preset colors.

IMPORTANT: V2 enhancement values are not yet runtime-proven at the time of this lock. Treat the original empty-key hostility fallback as proven; treat V2 cyan/fade/persistence tuning as the current next test.

---

# SP1 next_safe_action — UPDATED

The old `R7.7.4 custom W2S` next action is superseded for the primary Biter-through-wall goal.

Next action:

1. Keep repaired `data3.pak` installed.
2. Use no old Sense Lua hooks.
3. Install/test `DLTB_SURVIVOR_SENSE_MASTER_V2_CYAN_INSTANT_PERSIST_READY.zip` as `data4.pak`.
4. Verify all of the following:
   - ordinary Biter is cyan through walls;
   - sleeping/resting Biter still highlights;
   - zombie/human highlight fade-in is nearly instant;
   - highlighted AI remains visible substantially longer when the player turns away and back;
   - far already-scanned AI no longer drops at the old ~200m visibility edge.
5. If any V2 tuning regresses the proven Biter-through-wall function, restore the proven empty-key fallback baseline immediately and change only one tuning variable at a time.
6. Do not return to live predicate/submit hooks unless static config is definitively insufficient for a new requirement.

---

# GREEN / proven after 2026-10-01

- Native candidate vector contains ordinary Biters.
- Empty-preset hostility fallback keyed by `""` is a working route.
- Ordinary Biters render through walls using native Survivor Sense.
- Resting/sleeping Biters also render through walls using the working route.
- Static PAK config is sufficient for the primary Biter-through-wall goal.
- Custom W2S is no longer required for the primary goal.

# Current unproven enhancement

- V2 electric-cyan Biter preset.
- 0.03 Sense smoothing.
- 60s AI highlight duration.
- 400m post-scan visibility distance.

These must receive user runtime confirmation before being moved to GREEN/proven.