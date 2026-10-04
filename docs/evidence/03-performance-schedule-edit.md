# Performance Schedule Editing — Development Record

**Date:** 2026-10-04

**Developer:** Jiachen Li (Productions module)

**Working branch:** `productions-a2` (local work; not yet pushed for this increment)

**Evidence session:** 2026-10-04 (Asia/Shanghai)

## Scope

Added a schedule overview at `/productions/<production_id>/schedule` and an
edit form at
`/productions/<production_id>/performances/<performance_id>/edit-schedule`.
Authorised users can correct a performance's date and start time. The route
checks that the performance belongs to the production in the URL and rejects
missing or malformed date/time input without saving it.

## Preservation boundary

This increment appends routes to `app/productions/routes.py` and adds new
template, test, and evidence files. It does not edit or delete existing source
lines or replace existing pages. The new schedule overview is independently
available by its URL because the existing navigation templates remain
untouched under the repository preservation instruction.

## Automated verification

Four additional tests cover the schedule view, a successful date/time update,
invalid input preserving the prior schedule, and rejection of a performance
that belongs to a different production.

Command:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest -q
```

Result:

```text
22 passed, 61 warnings in 1.69s
```

`git diff --check` also completed without whitespace errors. The warnings are
the existing SQLAlchemy `datetime.utcnow()` deprecation warning from the
shared model default; this increment did not modify that baseline code.

## Screenshot evidence

No screenshot is claimed as a saved repository file in this record. Browser
screenshots may be added to the local evidence folder when they can be saved
there without changing existing evidence files.

During the evidence session, browser screenshots were captured and displayed
in the development conversation for:

1. the schedule list before editing (`17 Oct 2026`, `19:30`);
2. the edit form with the existing date and time prefilled; and
3. the saved schedule (`18 Oct 2026`, `20:00`) with the success message.

The current browser capture tool returns screenshots to the conversation but
does not provide a supported way to write those image bytes into this local
evidence directory. The screenshots are therefore visible in the conversation,
but no local PNG is claimed. For submission-ready PNGs, capture the same views
from a normal browser using the evidence register's filenames.

## Git handoff

The prior increment is commit `1bfa381` and is present on the user's
`origin/New-module-development` branch. This schedule-edit increment is being
committed on local `productions-a2` for the same integration branch.
