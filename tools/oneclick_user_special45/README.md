# USER HIGH LOOT SPECIAL45 one-click installer source

This directory preserves the text/source side of the final USER HIGH LOOT SPECIAL45 one-click installer created during the development chat.

It intentionally does **not** contain `data2_payload.pak` because built gameplay PAKs remain local-only.

To prepare the canonical payload on a fresh 1.71E machine, run from repository root:

```bat
tools\BOOTSTRAP_1.71E_USER_SPECIAL45.cmd
```

The verified payload will be produced with expected SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

For this archived one-click installer layout, copy that verified payload beside these files as:

`tools\oneclick_user_special45\data2_payload.pak`

Then use:

- `INSTALL_ONE_CLICK.cmd`
- `CHECK_STATUS.cmd`
- `UNINSTALL_ALL_ONE_CLICK.cmd`

The installer builds recipe `data3.pak` from the currently installed official `data0.pak` / `data1.pak`, checks known hashes, backs up saves, performs verified replacement, and rolls back on failure.

Current runtime-preferred workflow remains `tools/runtime_switcher/` because NORMAL <-> CO-OP MultiMod switching is runtime proven with the sibling remaining vanilla.

Do not commit the generated `data2_payload.pak`.
