"""Add-only production-management pages for duration-aware A2 workflows."""

from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.models import Assignment, CrewCall, Performance, Production, db

bp = Blueprint("production_extensions", __name__)


def _parse_duration(raw_value):
    try:
        duration = int(raw_value)
    except (TypeError, ValueError):
        return None, "Duration must be a whole number of minutes."
    if duration <= 0:
        return None, "Duration must be greater than 0 minutes."
    return duration, None


def _read_crew_call_rows(form):
    roles = form.getlist("role")
    counts = form.getlist("count")
    rows = []
    errors = []

    for index in range(max(len(roles), len(counts))):
        role = roles[index].strip() if index < len(roles) else ""
        raw_count = counts[index].strip() if index < len(counts) else ""
        if not role and raw_count == "":
            continue
        try:
            count = int(raw_count)
        except (TypeError, ValueError):
            errors.append("Enter a valid whole number for the crew-call headcount.")
            continue
        if not role:
            errors.append("Enter a role for each crew-call headcount.")
            continue
        if len(role) > 80:
            errors.append("Crew-call role names must be 80 characters or fewer.")
            continue
        if count <= 0:
            errors.append("Headcount for each crew-call role must be greater than 0.")
            continue
        rows.append((role, count))
    return rows, errors


def _crew_call_form_values(form):
    roles = form.getlist("role") or [""]
    counts = form.getlist("count") or ["0"]
    return [
        {
            "role": roles[index] if index < len(roles) else "",
            "count": counts[index] if index < len(counts) else "0",
        }
        for index in range(max(len(roles), len(counts)))
    ]


def _overlapping_performance_ids():
    performances = Performance.query.filter(
        Performance.duration_minutes.isnot(None), Performance.duration_minutes > 0
    ).order_by(Performance.date, Performance.start_time).all()
    overlaps = set()
    for index, first in enumerate(performances):
        for second in performances[index + 1 :]:
            if second.starts_at >= first.ends_at:
                break
            if first.starts_at < second.ends_at and second.starts_at < first.ends_at:
                overlaps.update((first.id, second.id))
    return overlaps


def _render_management(production, status=200, error_message=None):
    return render_template(
        "production_extensions/manage.html",
        production=production,
        performance_overlap_ids=_overlapping_performance_ids(),
        performance_assignment_counts={
            performance.id: len(performance.assignments)
            for performance in production.performances
        },
        production_assignment_count=sum(
            len(performance.assignments) for performance in production.performances
        ),
        error_message=error_message,
    ), status


@bp.route("/productions/<int:production_id>/management")
def manage_production_enhanced(production_id):
    return _render_management(db.get_or_404(Production, production_id))


@bp.route("/productions/<int:production_id>/performances/new-enhanced", methods=["GET", "POST"])
def create_performance_enhanced(production_id):
    production = db.get_or_404(Production, production_id)
    if request.method == "POST":
        errors = []
        try:
            date = datetime.strptime(request.form.get("date", ""), "%Y-%m-%d").date()
            start_time = datetime.strptime(request.form.get("start_time", ""), "%H:%M").time()
        except ValueError:
            date = start_time = None
            errors.append("Date and start time are required.")

        duration, duration_error = _parse_duration(request.form.get("duration_minutes"))
        if duration_error:
            errors.append(duration_error)
        crew_calls, crew_errors = _read_crew_call_rows(request.form)
        errors.extend(crew_errors)
        if errors:
            return render_template(
                "production_extensions/performance_form.html",
                production=production,
                errors=errors,
                form_values=request.form,
                crew_call_rows=_crew_call_form_values(request.form),
            ), 400

        performance = Performance(
            production=production,
            date=date,
            start_time=start_time,
            duration_minutes=duration,
        )
        performance.crew_calls.extend(
            CrewCall(role=role, count=count) for role, count in crew_calls
        )
        db.session.add(performance)
        db.session.commit()
        return redirect(url_for("productions.production_detail", production_id=production.id))

    return render_template(
        "production_extensions/performance_form.html",
        production=production,
        crew_call_rows=[{"role": "", "count": "0"}],
    )


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/edit-enhanced",
    methods=["GET", "POST"],
)
def edit_performance_enhanced(production_id, performance_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    if performance.production_id != production.id:
        abort(404)

    if request.method == "POST":
        try:
            date = datetime.strptime(request.form.get("date", ""), "%Y-%m-%d").date()
            start_time = datetime.strptime(request.form.get("start_time", ""), "%H:%M").time()
        except ValueError:
            date = start_time = None
            error_message = "Date and start time are required."
        else:
            duration, error_message = _parse_duration(request.form.get("duration_minutes"))

        if error_message:
            return render_template(
                "production_extensions/edit_schedule.html",
                production=production,
                performance=performance,
                form_values=request.form,
                error_message=error_message,
            ), 400

        performance.date = date
        performance.start_time = start_time
        performance.duration_minutes = duration
        db.session.commit()
        flash("Performance schedule updated.")
        return redirect(url_for("production_extensions.manage_production_enhanced", production_id=production.id))

    return render_template(
        "production_extensions/edit_schedule.html",
        production=production,
        performance=performance,
    )


@bp.route("/productions/<int:production_id>/crew-calls-enhanced", methods=["GET", "POST"])
def manage_crew_calls_enhanced(production_id):
    production = db.get_or_404(Production, production_id)
    if request.method == "POST":
        performance = db.get_or_404(Performance, request.form.get("performance_id", type=int))
        if performance.production_id != production.id:
            abort(404)
        rows, errors = _read_crew_call_rows(request.form)
        if len(rows) != 1 and not errors:
            errors.append("Add one crew-call role at a time.")
        if errors:
            return render_template(
                "production_extensions/crew_calls.html",
                production=production,
                error_message=" ".join(errors),
                form_performance_id=performance.id,
                form_values=request.form,
            ), 400
        role, count = rows[0]
        db.session.add(CrewCall(performance=performance, role=role, count=count))
        db.session.commit()
        flash("Crew requirement added.")
        return redirect(url_for("production_extensions.manage_crew_calls_enhanced", production_id=production.id))

    return render_template("production_extensions/crew_calls.html", production=production)


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/crew-calls/<int:crew_call_id>/edit-enhanced",
    methods=["GET", "POST"],
)
def edit_crew_call_enhanced(production_id, performance_id, crew_call_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    crew_call = db.get_or_404(CrewCall, crew_call_id)
    if performance.production_id != production.id or crew_call.performance_id != performance.id:
        abort(404)

    if request.method == "POST":
        role = request.form.get("role", "").strip()
        raw_count = request.form.get("count", "").strip()
        try:
            count = int(raw_count)
        except ValueError:
            count = None
        if count is None:
            error_message = "Enter a valid whole number for the crew-call headcount."
        elif not role:
            error_message = "Role is required."
        elif len(role) > 80:
            error_message = "Crew-call role names must be 80 characters or fewer."
        elif count <= 0:
            error_message = "Headcount for this role must be greater than 0."
        else:
            crew_call.role = role
            crew_call.count = count
            db.session.commit()
            flash("Crew call updated.")
            return redirect(url_for("production_extensions.manage_crew_calls_enhanced", production_id=production.id))
        return render_template(
            "production_extensions/edit_crew_call.html",
            production=production,
            performance=performance,
            crew_call=crew_call,
            form_values=request.form,
            error_message=error_message,
        ), 400

    return render_template(
        "production_extensions/edit_crew_call.html",
        production=production,
        performance=performance,
        crew_call=crew_call,
    )


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/crew-calls/<int:crew_call_id>/delete-enhanced",
    methods=["POST"],
)
def delete_crew_call_enhanced(production_id, performance_id, crew_call_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    crew_call = db.get_or_404(CrewCall, crew_call_id)
    if performance.production_id != production.id or crew_call.performance_id != performance.id:
        abort(404)
    if request.form.get("confirmed") != "yes":
        abort(400, "Deletion confirmation is required.")
    if Assignment.query.filter_by(performance_id=performance.id, role=crew_call.role).count():
        return render_template(
            "production_extensions/crew_calls.html",
            production=production,
            error_message="Remove assignments for this role before deleting the requirement.",
            form_performance_id=performance.id,
        ), 409
    db.session.delete(crew_call)
    db.session.commit()
    flash("Crew requirement deleted.")
    return redirect(url_for("production_extensions.manage_crew_calls_enhanced", production_id=production.id))


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/delete-enhanced",
    methods=["POST"],
)
def delete_performance_enhanced(production_id, performance_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    if performance.production_id != production.id:
        abort(404)
    if request.form.get("confirmed") != "yes":
        abort(400, "Deletion confirmation is required.")
    db.session.delete(performance)
    db.session.commit()
    flash("Performance deleted.")
    return redirect(url_for("production_extensions.manage_production_enhanced", production_id=production.id))


@bp.route("/productions/<int:production_id>/delete-enhanced", methods=["POST"])
def delete_production_enhanced(production_id):
    production = db.get_or_404(Production, production_id)
    if request.form.get("confirmed") != "yes":
        abort(400, "Deletion confirmation is required.")
    db.session.delete(production)
    db.session.commit()
    flash("Production deleted.")
    return redirect(url_for("productions.list_productions"))
