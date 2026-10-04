from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import Assignment, Performance, Volunteer, db, find_assignment

bp = Blueprint("assignments", __name__)


@bp.route("/assignments")
def list_assignments():
    query = Assignment.query
    performance_id = request.args.get("performance_id", type=int)
    volunteer_id = request.args.get("volunteer_id", type=int)
    if performance_id:
        query = query.filter(Assignment.performance_id == performance_id)
    if volunteer_id:
        query = query.filter(Assignment.volunteer_id == volunteer_id)
    assignments = query.order_by(Assignment.id.desc()).all()
    volunteers = Volunteer.query.order_by(Volunteer.name).all()
    performances = Performance.query.order_by(Performance.date, Performance.start_time).all()
    return render_template(
        "assignments/list.html",
        assignments=assignments,
        volunteers=volunteers,
        performances=performances,
        filter_performance=performance_id,
        filter_volunteer=volunteer_id,
    )


@bp.route("/assignments/new", methods=["GET", "POST"])
def create_assignment():
    volunteers = Volunteer.query.filter_by(is_active=True).order_by(Volunteer.name).all()
    performances = Performance.query.order_by(Performance.date, Performance.start_time).all()
    if request.method == "POST":
        try:
            volunteer_id = int(request.form["volunteer_id"])
            performance_id = int(request.form["performance_id"])
        except (KeyError, ValueError):
            flash("Volunteer and performance are required.", "error")
            return render_template("assignments/form.html", volunteers=volunteers, performances=performances), 400
        role = request.form.get("role", "").strip()
        if not role:
            flash("Role is required.", "error")
            return render_template("assignments/form.html", volunteers=volunteers, performances=performances), 400

        if find_assignment(volunteer_id, performance_id) is not None:
            flash(
                "Refused: this volunteer already holds a role in that performance "
                "(one role per performance).",
                "error",
            )
            return render_template("assignments/form.html", volunteers=volunteers, performances=performances), 409

        assignment = Assignment(
            volunteer_id=volunteer_id,
            performance_id=performance_id,
            role=role,
            status="unconfirmed",
        )
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for("assignments.list_assignments"))
    return render_template("assignments/form.html", volunteers=volunteers, performances=performances)


@bp.route("/assignments/<int:assignment_id>/delete", methods=["POST"])
def delete_assignment(assignment_id):
    assignment = db.get_or_404(Assignment, assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    return redirect(url_for("assignments.list_assignments"))


@bp.route("/assignments/<int:assignment_id>/toggle-status", methods=["POST"])
def toggle_status(assignment_id):
    assignment = db.get_or_404(Assignment, assignment_id)
    assignment.status = "confirmed" if assignment.status == "unconfirmed" else "unconfirmed"
    db.session.commit()
    return redirect(url_for("assignments.list_assignments"))


@bp.route("/assignments/roster")
def roster():
    performances = Performance.query.order_by(Performance.date, Performance.start_time).all()
    return render_template("assignments/roster.html", performances=performances)
