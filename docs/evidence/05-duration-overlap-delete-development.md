# Performance Duration, Crew-Call Validation, and Deletion Confirmation

**Date:** 2026-10-04 (Asia/Shanghai)
**Role:** Jiachen Li — Productions module
**Branch:** `feature/productions-management` (local only)
**Base commit:** `2564889` (`Merge pull request #7 from Dloperity/New-module-development`)
**Jira:** No ticket reference supplied.

This record includes an initial implementation checkpoint and a later
source-preservation audit. The initial test and browser results below are
historical; they do not verify the current add-only implementation. The latest
status is in the follow-up audit section.

## Scope and preservation

Implemented within Productions: performance duration and end-time display,
same-date/time overlap warnings, dynamic crew-call rows and headcount controls,
production/performance editing and deletion, and English validation and delete
confirmation messages. Existing databases receive a nullable duration column;
existing performance rows are preserved and are not assigned guessed durations.

The homepage (`app/templates/index.html`) and the Volunteers and Assignments
modules (`app/volunteers/`, `app/assignments/`) have no content diff. The shared
`app/templates/base.html` has no textual diff. Shared model/application setup
changes are limited to the additive Performance duration field and its
idempotent schema migration; there are no Volunteers or Assignments behavior
changes.

## Historical verification — initial implementation

- JavaScript syntax: `node --check` passed for both new Production scripts.
- Python syntax compilation passed for all changed Python files.
- Full automated suite: `45 passed, 132 warnings in 3.68s`.
- Warnings are SQLAlchemy deprecations for the existing `datetime.utcnow()`
  default; this feature did not change those defaults.
- Browser checks used a temporary SQLite database and fictional data only.
  The time preview displayed `19:00 - 20:30`; two same-date overlapping shows
  displayed warnings; zero crew headcount displayed a red message and blocked
  the form; the delete dialog showed Yes/No and choosing No preserved the show.
- The database migration test confirms the legacy performance row remains and
  its new duration stays `NULL` until an administrator edits it.

## Historical screenshot evidence — initial implementation

Authentic local-browser JPEG screenshots are in this folder:

1. `05-crew-call-validation-error.jpg`
2. `06-performance-duration-and-roles.jpg`
3. `07-overlap-warning.jpg`
4. `08-delete-confirmation.jpg`

The names shown are synthetic. These images are ignored by Git under the
existing evidence-folder ignore rule and are not yet in a commit.

## Git handoff

No commit or push was performed. No changes were sent to
`ThirstyCoco/tinshed-players`. The user should inspect the local diff first;
publication requires explicit approval.

## Follow-up source-preservation audit — 2026-10-04

After the screenshot session, a strict audit restored the pre-existing
Productions routes, templates, and original test files to the `2564889` tree.
The screenshots above document the earlier local UI state and do not mean the
feature remains wired into the app after that restoration. At this audit
checkpoint, the prior baseline plus the additive duration model/migration tests
passed **37 tests**. The user then authorized restoration of the original
`from datetime import datetime` statement. That statement is restored verbatim;
`timedelta` is imported on a separate additive line. The enhanced Productions
workflow now lives in the new `app/production_extensions.py` blueprint and new
`app/templates/production_extensions/` templates. The existing
`productions.create_performance` endpoint and URL are retained as a compatibility
entry point but now delegate to the enhanced duration-aware handler. The old
fixed-two-role `app/templates/productions/performance_form.html` has been
removed; the original production detail button therefore opens the enhanced
single-row/dynamic-role form without changing its link or the detail table.

New isolated tests are in `tests/test_production_extensions.py`. A fresh test
run could not be completed in this environment: the repository `.venv` Python
launcher points to a missing system Python 3.12 installation, and the bundled
Python has neither pytest nor the app dependencies (the repository does list
pytest in `requirements.txt`). Python syntax-only compilation, both JavaScript
syntax checks, and `git diff --check` passed; runtime and browser verification
are pending a working project Python environment. Screenshots listed above were captured before the source-preserving
restoration and therefore are historical evidence only, not proof of the current
new routes.

## Legacy form replacement — 2026-10-05

Updated the old add-performance URL to use the enhanced form and removed its
obsolete fixed-two-row template. The production test now supplies the required
duration and checks that the legacy URL serves the duration/dynamic-role form.
The source and JavaScript syntax checks pass, but pytest and a fresh browser
screenshot remain unavailable until the project's Python environment is
repaired; the earlier screenshots remain historical only.

## Crew-call row sizing — 2026-10-05

Adjusted only the new performance form's crew-call rows to Bootstrap's
responsive grid, using the previous form's 8/12 role-column proportion and
compact form controls. The headcount stepper occupies 3/12 and the remove
control 1/12 on desktop; these controls stack on narrow screens. No shared
layout, homepage, volunteer, assignment, route, or validation code changed.
Static review passed; a fresh browser screenshot could not be captured because
the local Python virtual-environment launcher remains unavailable.
