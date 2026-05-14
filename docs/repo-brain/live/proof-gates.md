# Proof Gates

## Gate 1 - Source Boundary

- Public Act 1 source only.
- No later-act source, workshop files, or unrelated engine artifacts.

## Gate 2 - ChoiceScript Shape

- `startup.txt` defines title, author, scene list, and stats.
- Scene list includes `startup`, all generated Act 1 chapter/optional scenes,
  and `act1_ending`.
- `choicescript_stats.txt` exposes the tracked variables.

## Gate 3 - Mechanical Consequence

- P0 focuses on complete route coverage rather than tuned stat gates.
- Every optional scene is reachable through at least one generated choice.
- The ending reports tracked route state and keeps stats available for the next
  mechanics pass.

## Gate 4 - Native Tests

- `quicktest.js` passes.
- `randomtest.js game=starforge_test num=10000 seed=0 showCoverage=false showChoices=false` passes.

## Gate 5 - Manual Smoke

- `web/mygame/index.html` opens in a browser through a local static server.
- A player can start Act 1, branch into optional scenes, and finish the Act 1
  route.
