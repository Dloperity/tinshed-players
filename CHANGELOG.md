# Changelog

All notable changes to the Tinshed Players crew rostering web application are documented in
this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Assignment editing (`GET/POST /assignments/<id>/edit`) with an Edit action on the assignment list, a
  dedicated edit template, a guard that refuses to move a volunteer into a performance where they
  already hold a role, and a guard that rejects inactive volunteers.
- `seed.py`, a small demo-data script for manual testing and screenshots.

### Planned (A3)
- Coverage-gap view that highlights crew-call roles which are still unfilled for a performance
  (the `CrewCall(role, count)` model added in 0.1.0 is already in place to support this).

## [0.2.0] - 2026-10-02 — A2: assignment views, confirmation status and roster

### Added
- Filtering on the assignment list by performance and by volunteer
  (`GET /assignments?performance_id=<id>&volunteer_id=<id>`), with a filter form that keeps the
  current selection and a Clear action.
- Confirm / unconfirm toggle for each assignment (`POST /assignments/<id>/toggle-status`), with a
  status badge shown on the assignment list.
- Roster view (`GET /assignments/roster`) that groups all assignments by performance and shows
  the role, volunteer and confirmation status, or "No one assigned yet." when a performance has
  no volunteers.

### Changed
- `list_assignments()` now applies the optional performance / volunteer filters and passes the
  selected values back to the template so the filter form stays in sync.
- The assignment list renders the confirmation status as a badge with a Confirm / Unconfirm
  action instead of plain text.

### Tests
- Added 3 tests (filtering by performance, confirming an assignment, roster grouping); the
  assignment module now has 8 tests and the suite totals 15 passing.

## [0.1.0] - 2026-09-19 — Skeleton

### Added
- Flask application factory `create_app()` with settings read from environment variables
  (`SECRET_KEY`, `DATABASE_URL`) and blueprints for volunteers, productions and assignments.
- Data model: `Volunteer`, `Production`, `Performance`, `CrewCall` and `Assignment`, including
  the one-role-per-performance unique constraint on `(volunteer_id, performance_id)`.
- Assignment skeleton: list, create (validation plus a friendly 409 refusal when the
  one-role-per-performance rule is violated) and delete.
- Test suite with a shared `seed` fixture; 5 assignment tests covering create, the rule refusal,
  the same volunteer in a different performance, and delete (suite total 12 passing).
- Configuration management and deployment files: `.env.example`, `.gitignore`, `render.yaml`
  (Render deployment) and `.github/workflows/ci.yml` (pytest on every push / pull request).
