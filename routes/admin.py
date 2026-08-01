from flask import Blueprint, render_template, redirect, url_for, session, request
from extensions import db
from models.user import User
from models.trek import Trek
from datetime import datetime

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="trek_staff").count()
    total_treks = Trek.query.count()
    total_bookings = 0

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings
    )

@admin.route("/admin/users")
def manage_users():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    return render_template("manage_users.html")

@admin.route("/admin/staff")
def manage_staff():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    pending_staff = User.query.filter_by(
        role="trek_staff",
        is_approved=False
    ).all()

    return render_template(
        "manage_staff.html",
        pending_staff=pending_staff
    )


@admin.route("/admin/staff/approve/<int:user_id>")
def approve_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    staff_member = db.session.get(User, user_id)

    if (
        staff_member is None
        or staff_member.role != "trek_staff"
        or staff_member.is_approved
    ):
        return "Invalid staff member.", 404

    staff_member.is_approved = True
    db.session.commit()

    return redirect(url_for("admin.manage_staff"))


@admin.route("/admin/staff/reject/<int:user_id>")
def reject_staff(user_id):
    return "Reject functionality coming soon."


@admin.route("/admin/treks")
def manage_treks():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    treks = Trek.query.all()

    return render_template(
        "manage_treks.html",
        treks=treks
    )


@admin.route("/admin/treks/add", methods=["GET", "POST"])
def add_trek():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    if request.method == "POST":

        trek_count = Trek.query.count() + 1
        public_id = f"TRK{trek_count:04d}"

        new_trek = Trek(
            public_id=public_id,
            name=request.form.get("name"),
            location=request.form.get("location"),
            difficulty=request.form.get("difficulty"),
            duration=int(request.form.get("duration")),
            available_slots=int(request.form.get("available_slots")),
            status="Pending",
            start_date=datetime.strptime(
                request.form.get("start_date"),
                "%Y-%m-%d"
            ).date(),
            end_date=datetime.strptime(
                request.form.get("end_date"),
                "%Y-%m-%d"
            ).date(),
            description=request.form.get("description"),
            price=float(request.form.get("price"))
        )

        db.session.add(new_trek)
        db.session.commit()

    return redirect(url_for("admin.manage_treks"))

@admin.route("/admin/treks/edit/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found.", 404

    if request.method == "POST":

        trek.name = request.form.get("name")
        trek.location = request.form.get("location")
        trek.difficulty = request.form.get("difficulty")
        trek.duration = int(request.form.get("duration"))
        trek.available_slots = int(request.form.get("available_slots"))
        trek.price = float(request.form.get("price"))
        trek.description = request.form.get("description")

        trek.start_date = datetime.strptime(
            request.form.get("start_date"),
            "%Y-%m-%d"
        ).date()

        trek.end_date = datetime.strptime(
            request.form.get("end_date"),
            "%Y-%m-%d"
        ).date()

        db.session.commit()

    return redirect(url_for("admin.manage_treks"))

@admin.route("/admin/treks/delete/<int:trek_id>")
def delete_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found.", 404

    db.session.delete(trek)
    db.session.commit()

    return redirect(url_for("admin.manage_treks"))