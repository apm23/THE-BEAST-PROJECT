# THE BEAST PROJECT

Development repository for a **Dying Light: The Beast** weapon-rarity, loot-gacha, and Legendary Ascension mod.

## Baseline

- Target game build: **VER. 1.71E**
- Initial state: fresh install, no mods installed
- Clean test save captured before mod development
- Repository stores only project-authored patches, configuration, tooling, and test records. Do **not** commit extracted proprietary game archives or user save files.

## Authority

Before changing the project, read these files in order:

1. `MASTER_STATE.md`
2. `PROJECT_CONTRACT.md`
3. `FEATURE_SPEC.md`
4. `TEST_MATRIX.md`

GitHub HEAD + `MASTER_STATE.md` are the authoritative project state.

## Workflow

```text
clean game baseline
    -> inspect only required vanilla definitions locally
    -> project patch/config
    -> validate
    -> build mod package
    -> in-game test
    -> persistence/uninstall test
    -> update MASTER_STATE
```

## Safety / cleanliness

Keep original game archives, extracted vanilla files, saves, and local install paths outside the public repository. See `.gitignore`.
