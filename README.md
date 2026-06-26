# starforge-choicescript-demo

The medical bay has six cots and four are taken. Worker 394 gets forty-eight hours
off-shift, unpaid, interest accruing at standard rates, and a waiver to sign. That
scene is one of 67 here, wired into a stat sheet that watches what you decide.

## What it does

[Starforge Canticles](https://www.royalroad.com/fiction/149065/starforge-canticles)
is a serialized speculative-fiction novel by Cessnya Lin. This repo takes the full
released Act 1 route and turns it into a playable ChoiceScript game: every main
chapter, the optional lettered scenes hanging off them, and five stats that track
the kind of person you're being about it — resolve, empathy, tech, lattice,
crew_trust, all starting at a neutral 50, plus a counter for scenes seen.

ChoiceScript is the stat-forward branch of the family. The Twine, Ren'Py, and Godot
builds tell the same Act 1 a different way; this one is the version where every
choice is a number moving on a sheet, and a test harness that plays the game ten
thousand times to make sure none of those choices walks you into a wall.

## Try it

One command. It runs the release gate — schema checks, a path-and-dead-letter audit,
then ChoiceScript's own quicktest and randomtest against the vendored engine:

```powershell
python tools\check_release.py
```

```
public-scope validation passed
ChoiceScript playtest audit
- scene_list entries: 67
- scene files: 68
- choices: 143
- stat mutations: 65
- scene refs: 143
- dead-letter marker hits: 0
playtest audit passed

== Public-scope validation ==
+ C:\Python314\python.exe tools/validate_public_scope.py

== Playtest path/dead-letter audit ==
+ C:\Python314\python.exe tools/playtest_audit.py

== ChoiceScript quicktest ==
+ node quicktest.js starforge_test
QUICKTEST PASSED

== ChoiceScript randomtest ==
+ node randomtest.js game=starforge_test num=10000 seed=0 showCoverage=false showChoices=false
RANDOMTEST PASSED

release gate passed
```

143 choices, 65 stat mutations, zero dead letters. randomtest sends 10,000 blind
playthroughs through the whole branch tree on a fixed seed; if any of them hit a
scene that doesn't exist or a `*goto` with nowhere to land, the gate fails and so
does the build. Green means the route holds.

For a clean strict local proof run, use
`python tools\check_release.py --clean --fail-on-generated`. In the local
five-repo cluster, use
`python tools\check_release.py --clean --fail-on-generated --regenerate` to
regenerate from `../starforge-narrative-tools/prose/act1` before validation.

## Live demo

The `web/` directory is a self-contained static ChoiceScript build — the vendored
runtime plus the generated Act 1 game. No build step, no server-side code, so it
deploys to Vercel as a static site.

- Deploy target: Vercel (static, no build). Config: [`vercel.json`](vercel.json)
  sets `outputDirectory: "web"` with no build command.
- Entry point: `web/index.html`, which redirects to `web/mygame/index.html`.

Deploy from this repo root with the Vercel CLI:

```bash
vercel deploy --prod
```

Or import the repo in the Vercel dashboard; the included `vercel.json` serves
`web/` directly with no framework preset.

<!-- live-url: (add the vercel url here once deployed) -->

## Run locally

```powershell
python -m http.server 8001 --directory web
```

Open `http://localhost:8001/mygame/index.html`.

## How it connects

Same Act 1, four playable shapes. This repo is the stat-game one; the rest of the
Starforge cluster does it differently:

- [starforge-narrative-tools](https://github.com/AthenaTheOwl/starforge-narrative-tools) — the public Act 1 corpus plus the conversion and validation tooling everything else feeds from.
- [starforge-twine-demo](https://github.com/AthenaTheOwl/starforge-twine-demo) — the full Act 1 route as a single-HTML Twine/SugarCube build.
- [starforge-renpy-demo](https://github.com/AthenaTheOwl/starforge-renpy-demo) — the Act 1 Ren'Py visual-novel copy.
- [starforge-rpg-prototype](https://github.com/AthenaTheOwl/starforge-rpg-prototype) — the Act 1 Godot RPG prototype copy.

## Layout

What's in the repo, and what's deliberately kept out:

- `web/mygame/` — the playable ChoiceScript source (67 scenes plus stats screen).
- `tools/generate_full_act1.py` — the source-to-scene generator.
- `tools/vendor/choicescript/` — the engine and test-harness snapshot.
- `tools/check_release.py` — the deterministic gate; `tools/playtest_audit.py` the path audit.
- repo-brain and spec docs under `docs/`.

Left out on purpose: unreleased later-act prose and spec content, runtime logs and
generated test output, and the Ren'Py / Godot / Twine build artifacts that live in
their own repos.

## License

MIT. See [LICENSE](LICENSE).
