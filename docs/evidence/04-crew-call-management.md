# Existing Performance Crew-Call Management — Development Record

**Date:** 2026-10-04

**Developer:** Jiachen Li (Productions module)

**Development branch:** `productions-a2` (local work branch; published counterpart:
`New-module-development` in the personal `Dloperity/tinshed-players` repository)

## Progress review

The productions module now supports creating productions and performances,
editing production titles, editing performance dates and times, editing
existing crew-call roles and counts, and deleting performances. A remaining
management gap was the inability to add or remove one crew requirement after a
performance had already been created.

## Scope added

Added a dedicated crew-call management view at
`/productions/<production_id>/crew-calls`. It lists each scheduled performance,
its requirements, edit links, and a form to add a role/count requirement.
Unassigned requirements can be removed individually. A deletion is refused
with HTTP 409 while assignments for that performance and role remain, so a
crew requirement cannot be removed while its corresponding roster entries
still exist.

## Preservation boundary

Only new route definitions were appended to `app/productions/routes.py`. The
page, test module, and this log are new files. No previously present source
line or template was edited or deleted. The dedicated page is directly
available at the URL above because existing navigation templates are kept
unchanged.

## Verification

Automated verification: `python -m pytest -q` — **28 passed**. The 81 warnings
are existing SQLAlchemy `datetime.utcnow()` deprecation warnings; no test failed.
`git diff --check` also passed.

Manual browser verification: opened the local manager for the synthetic
“Evidence Demo Production — Revised” and added “Stage Manager” with a count of
2. The page showed the success notice and the new requirement alongside the
existing “Sound Manager — 3 required” entry. No deletion action was performed
in the browser; the assignment-protection behavior is covered by an automated
test that expects HTTP 409 and verifies that both the requirement and linked
assignment remain.

Screenshot: the post-add page was captured and shown inline in the development
conversation. The browser screenshot interface did not provide a direct
workspace PNG path, and its attempted browser-side save was blocked by browser
security policy. Therefore no PNG file is claimed as a repository artifact;
the screenshot should be manually saved from the conversation if a local image
file is required for the final evidence pack.

## Publication record

At the initial handoff, this increment was still uncommitted on local
`productions-a2`; no push had taken place at that point. It was subsequently
committed as `23007776a8fc6e42990d52107666c31c8c05ed93` on 2026-10-04 and pushed
to the personal repository's `New-module-development` branch. The team
repository `ThirstyCoco/tinshed-players` was not changed by that push.

The publication-status correction in this record was committed as
`ee8b49445c26a242e7a9e9bc939413ce2bf796ed` on 2026-10-04 and pushed to the same
personal branch.

## Integration validation

On 2026-10-04, the personal source branch at `ee8b494` was merged without a
commit into an isolated local worktree based on the proposed target branch
`ThirstyCoco/tinshed-players:feature/productions-crewcall` at `95c00d9`.
Git completed the merge automatically with no file conflicts. Running
`python -m pytest -q` against the combined tree produced **36 passed** and 104
SQLAlchemy `datetime.utcnow()` deprecation warnings. This was a local
validation only; it did not modify the target branch on GitHub.
