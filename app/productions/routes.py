from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import CrewCall, Performance, Production, db

bp = Blueprint("productions", __name__)


@bp.route("/productions")
def list_productions():
    productions = Production.query.order_by(Production.id.desc()).all()
    return render_template("productions/list.html", productions=productions)


@bp.route("/productions/new", methods=["GET", "POST"])
def create_production():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return render_template("productions/form.html"), 400
        production = Production(title=title)
        db.session.add(production)
        db.session.commit()
        return redirect(url_for("productions.list_productions"))
    return render_template("productions/form.html")


@bp.route("/productions/<int:production_id>")
def production_detail(production_id):
    production = db.get_or_404(Production, production_id)
    return render_template("productions/detail.html", production=production)


@bp.route("/productions/<int:production_id>/performances/new", methods=["GET", "POST"])
def create_performance(production_id):
    # Keep the original URL/endpoint for existing callers, but use the
    # duration-aware form and validation as the single implementation.
    from app.production_extensions import create_performance_enhanced

    return create_performance_enhanced(production_id)


# A2 Production-management routes supplement the duration-aware create route.
@bp.route("/productions/<int:production_id>/manage")
def manage_production(production_id):
    production = db.get_or_404(Production, production_id)
    return render_template("productions/manage.html", production=production)


@bp.route("/productions/<int:production_id>/edit-title", methods=["GET", "POST"])
def edit_production_title(production_id):
    production = db.get_or_404(Production, production_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return render_template("productions/edit_title.html", production=production), 400
        production.title = title
        db.session.commit()
        flash("Production title updated.")
        return redirect(url_for("productions.manage_production", production_id=production.id))
    return render_template("productions/edit_title.html", production=production)


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/delete",
    methods=["POST"],
)
def delete_managed_performance(production_id, performance_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    if performance.production_id != production.id:
        return "Performance not found for this production.", 404

    db.session.delete(performance)
    db.session.commit()
    flash("Performance deleted.")
    return redirect(url_for("productions.manage_production", production_id=production.id))


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/crew-calls/<int:crew_call_id>/edit",
    methods=["GET", "POST"],
)
def edit_crew_call(production_id, performance_id, crew_call_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    crew_call = db.get_or_404(CrewCall, crew_call_id)
    if performance.production_id != production.id or crew_call.performance_id != performance.id:
        return "Crew call not found for this performance.", 404

    if request.method == "POST":
        role = request.form.get("role", "").strip()
        try:
            count = int(request.form.get("count", ""))
        except (TypeError, ValueError):
            count = 0

        if not role:
            flash("Role is required.", "error")
            return render_template(
                "productions/edit_crew_call.html",
                production=production,
                performance=performance,
                crew_call=crew_call,
            ), 400
        if count < 1:
            flash("Required crew count must be at least 1.", "error")
            return render_template(
                "productions/edit_crew_call.html",
                production=production,
                performance=performance,
                crew_call=crew_call,
            ), 400

        crew_call.role = role
        crew_call.count = count
        db.session.commit()
        flash("Crew call updated.")
        return redirect(url_for("productions.manage_production", production_id=production.id))

    return render_template(
        "productions/edit_crew_call.html",
        production=production,
        performance=performance,
        crew_call=crew_call,
    )




# Additional A2 extension: performance schedule editing without changing
# the original production routes or templates.
@bp.route("/productions/<int:production_id>/schedule")
def production_schedule(production_id):
    production = db.get_or_404(Production, production_id)
    return render_template("productions/schedule.html", production=production)


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/edit-schedule",
    methods=["GET", "POST"],
)
def edit_performance_schedule(production_id, performance_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    if performance.production_id != production.id:
        return "Performance not found for this production.", 404

    if request.method == "POST":
        try:
            date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
            start_time = datetime.strptime(request.form["start_time"], "%H:%M").time()
        except (KeyError, ValueError):
            flash("Date and start time are required (YYYY-MM-DD, HH:MM).", "error")
            return render_template(
                "productions/edit_performance_schedule.html",
                production=production,
                performance=performance,
            ), 400

        performance.date = date
        performance.start_time = start_time
        db.session.commit()
        flash("Performance schedule updated.")
        return redirect(url_for("productions.production_schedule", production_id=production.id))

    return render_template(
        "productions/edit_performance_schedule.html",
        production=production,
        performance=performance,
    )


# Additional A2 extension: manage crew-call requirements on existing
# performances without altering earlier routes or pages.
@bp.route("/productions/<int:production_id>/crew-calls")
def manage_crew_calls(production_id):
    production = db.get_or_404(Production, production_id)
    return render_template("productions/crew_calls.html", production=production)


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/crew-calls/new",
    methods=["POST"],
)
def create_crew_call(production_id, performance_id):
    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    if performance.production_id != production.id:
        return "Performance not found for this production.", 404

    role = request.form.get("role", "").strip()
    try:
        count = int(request.form.get("count", ""))
    except (TypeError, ValueError):
        count = 0

    if not role or len(role) > 80:
        flash("Role is required and must be 80 characters or fewer.", "error")
        return render_template("productions/crew_calls.html", production=production), 400
    if count < 1:
        flash("Required crew count must be at least 1.", "error")
        return render_template("productions/crew_calls.html", production=production), 400

    db.session.add(CrewCall(performance=performance, role=role, count=count))
    db.session.commit()
    flash("Crew requirement added.")
    return redirect(url_for("productions.manage_crew_calls", production_id=production.id))


@bp.route(
    "/productions/<int:production_id>/performances/<int:performance_id>/crew-calls/<int:crew_call_id>/delete",
    methods=["POST"],
)
def delete_crew_call(production_id, performance_id, crew_call_id):
    from app.models import Assignment

    production = db.get_or_404(Production, production_id)
    performance = db.get_or_404(Performance, performance_id)
    crew_call = db.get_or_404(CrewCall, crew_call_id)
    if performance.production_id != production.id or crew_call.performance_id != performance.id:
        return "Crew call not found for this performance.", 404

    linked_assignments = Assignment.query.filter_by(
        performance_id=performance.id,
        role=crew_call.role,
    ).count()
    if linked_assignments:
        flash(
            "Remove assignments for this role before deleting its crew requirement.",
            "error",
        )
        return render_template("productions/crew_calls.html", production=production), 409

    db.session.delete(crew_call)
    db.session.commit()
    flash("Crew requirement deleted.")
    return redirect(url_for("productions.manage_crew_calls", production_id=production.id))
