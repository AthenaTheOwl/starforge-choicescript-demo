# Architecture Map

`starforge-choicescript-demo` is the full Act 1 stat-forward choice-game
adaptation in the Starforge portfolio cluster.

## Boundaries

- Public source is read from `../starforge-narrative-tools/prose/act1`.
- Playable generated source lives in `web/mygame`.
- `tools/generate_full_act1.py` regenerates the route from the public Act 1
  prose files.
- ChoiceScript engine/test harness is vendored under `tools/vendor/choicescript`.
- `tools/check_release.py` mirrors `web/mygame` into the vendored harness for
  quicktest/randomtest, then removes the temporary mirror.
- No Ren'Py, Godot, or Twine build artifacts belong in this repo.

## Data Flow

1. Released Act 1 source files are parsed into main chapters and optional
   lettered scenes.
2. `startup.txt` initializes title, author, stats, and scene list.
3. Generated chapter scenes expose optional siblings, then rejoin the main
   spine.
4. ChoiceScript quicktest checks syntax/reachability.
5. ChoiceScript randomtest runs 10,000 seeded paths.
