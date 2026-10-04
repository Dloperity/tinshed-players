# Local Browser Validation — Productions Management

**Date:** 2026-10-03

**Branch:** `productions-a2` (local only)
**Environment:** local Flask development server at `http://127.0.0.1:5000`

## Purpose

Confirm that the new production-management routes work through the browser,
not only through Flask's test client. The test values below are intentionally
generic and contain no personal information.

## Test data created locally

- Production: `Evidence Demo Production`
- Performance: `17 Oct 2026`, `19:30`
- Initial crew requirement: `Sound Operator`, `2`

The application created this data only in the local SQLite development
database. It is not a tracked repository artifact and has not been committed
or pushed.

## Executed scenarios and observed results

| Scenario | Action | Observable result |
| --- | --- | --- |
| Management display | Opened `/productions/1/manage` | The production, its 17 Oct 2026 19:30 performance, `Sound Operator: 2 required`, edit link, and delete button were displayed. |
| Edit title | Used the title-edit form to change the name to `Evidence Demo Production — Revised` | Redirected to management view with the flash message `Production title updated.` and the revised heading. |
| Edit crew requirement | Used the crew-call edit form to change role and count to `Sound Manager` and `3` | Redirected to management view with the flash message `Crew call updated.` and `Sound Manager: 3 required` displayed. |

## Screenshot handling

Full-page browser screenshots were rendered during the local verification
session for the management view, title update, and crew-call update. The
available browser automation channel can render those images for review but
cannot persist its raw screenshot bytes into `docs/evidence/` as PNG files.
Therefore no image is falsely recorded as a local file. To create the
corresponding local PNG evidence, open the same local page in a normal browser
or VS Code preview and capture it using the agreed names from the evidence
register (for example, `02-production-edit.png` and
`04-crew-call-edit.png`).

## Related automated verification

The full suite also passed in the same working tree:

```text
18 passed, 48 warnings in 1.51s
```

See `01-productions-management-extension.md` for the test command and scope.
