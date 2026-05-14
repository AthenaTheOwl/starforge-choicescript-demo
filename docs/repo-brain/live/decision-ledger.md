# Decision Ledger

## D-001 - Keep ChoiceScript Separate

Decision: ChoiceScript is its own repo rather than a mode inside Twine.

Reason: ChoiceScript proves a different engine claim: visible stats, automated
branch testing, and a CYOA-style flow.

## D-002 - Vendor Engine Snapshot

Decision: The ChoiceScript engine/test harness is vendored under
`tools/vendor/choicescript`.

Reason: The engine is plain JavaScript and quicktest/randomtest are the native
verification tools.

## D-003 - Mirror Source Into Harness

Decision: The release gate copies `web/mygame` into a temporary vendored test
game before running quicktest/randomtest.

Reason: This keeps root `web/mygame` as the source of truth while preserving
ChoiceScript's expected test-runner directory shape.
