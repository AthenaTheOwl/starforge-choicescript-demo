# Verification scope — October 18, 2026

`python tools/check_release.py` passed public-scope validation, the route
audit, ChoiceScript quicktest and randomtest. The audit counted 143 choices,
65 stat mutations and no explicit dead-letter markers. Randomtest completed
10,000 iterations with seed 0. The engine source and published scenes were
unchanged; the temporary test-game copy was removed by the gate.

All 65 counted `*set` lines are the `scenes_seen +1` counter. Every choice
option leads to a `*goto_scene`; none sets or checks a stat. The five
character stats (resolve, empathy, tech, lattice, crew_trust) are created at
50 in `startup.txt` and shown on the stats screen, but no story scene changes
or reads them. Quicktest and randomtest therefore cover routing and
reachability only; this build has no stat logic for them to exercise.

A seeded random run is repeatable sampling. It does not prove that every
possible choice sequence or narrative payoff works. Review coverage and add a
deliberate path when an important branch is missed.
