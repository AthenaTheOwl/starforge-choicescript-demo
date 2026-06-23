# No. 18 - starforge-choicescript-demo

[Starforge Canticles](https://www.royalroad.com/fiction/149065/starforge-canticles)
is a serialized speculative-fiction novel by Cessnya Lin. This repo adapts the
full released Act 1 route into a ChoiceScript demo with visible stats and
automated branch testing.

The repo is separate from the Twine, Ren'Py, and Godot versions. ChoiceScript
proves the stat-forward choice-game path; it is not the Twine single-HTML
build, Ren'Py visual novel, or Godot RPG prototype.

## Live demo

The `web/` directory is a fully self-contained, static ChoiceScript build (the
vendored ChoiceScript runtime plus the generated Act 1 game). It needs no build
step and no server-side code, so it deploys to Vercel as a static site.

- Deploy target: Vercel (static, no build). Config: [`vercel.json`](vercel.json)
  sets `outputDirectory: "web"` with no build command.
- Entry point: `web/index.html`, which redirects to `web/mygame/index.html`.

Deploy from this repo root with the Vercel CLI:

```bash
vercel deploy --prod
```

Or import the repo in the Vercel dashboard; the included `vercel.json` serves
`web/` directly with no framework preset.

## Run locally

```powershell
python -m http.server 8001 --directory web
```

Open `http://localhost:8001/mygame/index.html`.

## Validate

```powershell
python tools\check_release.py
```

The deterministic gate runs public-scope validation, audits scene-list/path and
dead-letter coverage, mirrors the generated game into the vendored ChoiceScript
test harness, then runs quicktest and randomtest. For a clean strict local proof
run, use
`python tools\check_release.py --clean --fail-on-generated`. In the local
five-repo cluster, use
`python tools\check_release.py --clean --fail-on-generated --regenerate` to
regenerate from `../starforge-narrative-tools/prose/act1` before validation.

## Cleanup boundary

Included:

- `web/mygame/` playable ChoiceScript source
- `tools/generate_full_act1.py` source-to-scene generator
- `tools/vendor/choicescript/` engine/test harness snapshot
- deterministic Python gate
- deterministic playtest/path audit
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
