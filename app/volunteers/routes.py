from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import Volunteer, db

bp = Blueprint("volunteers", __name__)


@bp.route("/volunteers")
def list_volunteers():
    volunteers = Volunteer.query.order_by(Volunteer.name).all()
    return render_template("volunteers/list.html", volunteers=volunteers)


@bp.route("/volunteers/new", methods=["GET", "POST"])
def create_volunteer():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Name is required.", "error")
            return render_template("volunteers/form.html"), 400
        volunteer = Volunteer(
            name=name,
            email=request.form.get("email", "").strip() or None,
            phone=request.form.get("phone", "").strip() or None,
        )
        db.session.add(volunteer)
        db.session.commit()
        return redirect(url_for("volunteers.list_volunteers"))
    return render_template("volunteers/form.html")


@bp.route("/volunteers/<int:volunteer_id>/edit", methods=["GET", "POST"])
def edit_volunteer(volunteer_id):
    volunteer = db.get_or_404(Volunteer, volunteer_id)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Name is required.", "error")
            return render_template("volunteers/form.html", volunteer=volunteer), 400
        volunteer.name = name
        volunteer.email = request.form.get("email", "").strip() or None
        volunteer.phone = request.form.get("phone", "").strip() or None
        db.session.commit()
        return redirect(url_for("volunteers.list_volunteers"))
    return render_template("volunteers/form.html", volunteer=volunteer)


@bp.route("/volunteers/<int:volunteer_id>/toggle", methods=["POST"])
def toggle_volunteer(volunteer_id):
    volunteer = db.get_or_404(Volunteer, volunteer_id)
    volunteer.is_active = not volunteer.is_active
    db.session.commit()
    return redirect(url_for("volunteers.list_volunteers"))