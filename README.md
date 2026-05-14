# No. 18 - starforge-choicescript-demo

[Starforge Canticles](https://www.royalroad.com/fiction/149065/starforge-canticles)
is a serialized speculative-fiction novel by Cessnya Lin. This repo adapts the
full released Act 1 route into a ChoiceScript demo with visible stats and
automated branch testing.

The repo is separate from the Twine, Ren'Py, and Godot versions. ChoiceScript
proves the stat-forward choice-game path; it is not the Twine single-HTML
build, Ren'Py visual novel, or Godot RPG prototype.

## Run locally

```powershell
python -m http.server 8001 --directory web
```

Open `http://localhost:8001/mygame/index.html`.

## Validate

```powershell
python tools\check_release.py
```

The deterministic gate runs public-scope validation, mirrors the generated game
into the vendored ChoiceScript test harness, then runs quicktest and randomtest.
In the local five-repo cluster, use `python tools\check_release.py --regenerate`
to regenerate from `../starforge-narrative-tools/prose/act1` before validation.

## Cleanup boundary

Included:

- `web/mygame/` playable ChoiceScript source
- `tools/generate_full_act1.py` source-to-scene generator
- `tools/vendor/choicescript/` engine/test harness snapshot
- deterministic Python gate
- repo-brain and spec docs

Excluded:

- unreleased later-act prose/spec content
- runtime logs or generated test output
- Ren'Py, Godot, or Twine build artifacts

## See also

Part of the Starforge cluster:

- [starforge-narrative-tools](https://github.com/AthenaTheOwl/starforge-narrative-tools) - public Act 1 corpus + conversion/validation tooling
- [starforge-renpy-demo](https://github.com/AthenaTheOwl/starforge-renpy-demo) - Act 1 Ren'Py narrative demo copy
- [starforge-rpg-prototype](https://github.com/AthenaTheOwl/starforge-rpg-prototype) - Act 1 Godot RPG prototype copy
- [starforge-twine-demo](https://github.com/AthenaTheOwl/starforge-twine-demo) - full Act 1 single-HTML Twine/SugarCube route
