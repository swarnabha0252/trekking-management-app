from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.user import User
from models.trek import Trek
from datetime import datetime
from models.booking import Booking
from sqlalchemy import or_, func

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    total_users = User.query.filter_by(
        role="user"
    ).count()

    total_staff = User.query.filter_by(
        role="trek_staff"
    ).count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    active_bookings = Booking.query.filter_by(
        status="Booked"
    ).count()

    completed_bookings = Booking.query.filter_by(
        status="Completed"
    ).count()

    cancelled_bookings = Booking.query.filter_by(
        status="Cancelled"
    ).count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings,
        active_bookings=active_bookings,
        completed_bookings=completed_bookings,
        cancelled_bookings=cancelled_bookings
    )
@admin.route("/admin/users")
def manage_users():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    users = User.query.filter_by(
        role="user"
    ).all()

    return render_template(
        "manage_users.html",
        users=users
    )

@admin.route("/admin/users/block/<int:user_id>", methods=["POST"])
def block_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    user = db.session.get(User, user_id)

    if user is None or user.role != "user":
        flash("User not found.", "danger")
        return redirect(url_for("admin.manage_users"))

    if user.is_blacklisted:
        flash("User is already blocked.", "warning")
        return redirect(url_for("admin.manage_users"))

    user.is_blacklisted = True

    db.session.commit()

    flash(
        f"User {user.name} has been blocked successfully.",
        "success"
    )

    return redirect(url_for("admin.manage_users"))


@admin.route("/admin/users/unblock/<int:user_id>", methods=["POST"])
def unblock_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    user = db.session.get(User, user_id)

    if user is None or user.role != "user":
        flash("User not found.", "danger")
        return redirect(url_for("admin.manage_users"))

    if not user.is_blacklisted:
        flash("User is already active.", "warning")
        return redirect(url_for("admin.manage_users"))

    user.is_blacklisted = False

    db.session.commit()

    flash(
        f"User {user.name} has been unblocked successfully.",
        "success"
    )

    return redirect(url_for("admin.manage_users"))

@admin.route("/admin/staff")
def manage_staff():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    active_staff = User.query.filter_by(
        role="trek_staff",
        is_approved=True
    ).order_by(
        User.id.asc()
    ).all()

    pending_staff = User.query.filter_by(
        role="trek_staff",
        is_approved=False
    ).order_by(
        User.id.asc()
    ).all()

    return render_template(
        "manage_staff.html",
        active_staff=active_staff,
        pending_staff=pending_staff
    )


@admin.route("/admin/staff/approve/<int:user_id>")
def approve_staff(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    staff_member = db.session.get(
        User,
        user_id
    )

    if staff_member is None:
        flash(
            "Staff member not found.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.role != "trek_staff":
        flash(
            "Invalid staff account.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.is_approved:
        flash(
            "This staff account is already approved.",
            "warning"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    staff_member.is_approved = True
    staff_member.is_blacklisted = False

    db.session.commit()

    flash(
        f"{staff_member.name}'s staff account has been approved successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_staff")
    )


@admin.route("/admin/staff/reject/<int:user_id>")
def reject_staff(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    staff_member = db.session.get(
        User,
        user_id
    )

    if staff_member is None:
        flash(
            "Staff member not found.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.role != "trek_staff":
        flash(
            "Invalid staff account.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.is_approved:
        flash(
            "This staff account has already been approved.",
            "warning"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    db.session.delete(staff_member)
    db.session.commit()

    flash(
        "Staff registration request rejected successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_staff")
    )


@admin.route("/admin/staff/block/<int:user_id>")
def block_staff(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    staff_member = db.session.get(
        User,
        user_id
    )

    if staff_member is None:
        flash(
            "Staff member not found.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.role != "trek_staff":
        flash(
            "Invalid staff account.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if not staff_member.is_approved:
        flash(
            "Pending staff accounts cannot be blocked.",
            "warning"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.is_blacklisted:
        flash(
            "This staff member is already blocked.",
            "warning"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    staff_member.is_blacklisted = True

    db.session.commit()

    flash(
        f"{staff_member.name} has been blocked successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_staff")
    )


@admin.route("/admin/staff/unblock/<int:user_id>")
def unblock_staff(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    staff_member = db.session.get(
        User,
        user_id
    )

    if staff_member is None:
        flash(
            "Staff member not found.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if staff_member.role != "trek_staff":
        flash(
            "Invalid staff account.",
            "danger"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if not staff_member.is_approved:
        flash(
            "This staff account is still pending approval.",
            "warning"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    if not staff_member.is_blacklisted:
        flash(
            "This staff member is already active.",
            "warning"
        )
        return redirect(
            url_for("admin.manage_staff")
        )

    staff_member.is_blacklisted = False

    db.session.commit()

    flash(
        f"{staff_member.name} has been unblocked successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_staff")
    )


@admin.route("/admin/treks")
def manage_treks():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    treks = Trek.query.all()

    approved_staff = User.query.filter_by(
        role="trek_staff",
        is_approved=True,
        is_blacklisted=False
    ).all()

    return render_template(
        "manage_treks.html",
        treks=treks,
        approved_staff=approved_staff
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
            booking_status="Closed",
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

@admin.route("/admin/treks/assign/<int:trek_id>/<int:staff_id>")
def assign_staff(trek_id, staff_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    staff = db.session.get(User, staff_id)

    if trek is None or staff is None:
        return "Not Found", 404

    trek.assigned_staff_id = staff.id
    trek.status = "Open"
    trek.booking_status = "Open"

    db.session.commit()

    return redirect(url_for("admin.manage_treks"))

@admin.route("/admin/treks/close-booking/<int:trek_id>")
def close_booking(trek_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found.", 404

    trek.booking_status = "Closed"

    db.session.commit()

    return redirect(url_for("admin.manage_treks"))

@admin.route("/admin/treks/reopen-booking/<int:trek_id>")
def reopen_booking(trek_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found.", 404

    if trek.available_slots > 0:
        trek.booking_status = "Open"

    db.session.commit()

    return redirect(url_for("admin.manage_treks"))

@admin.route("/admin/bookings")
def manage_bookings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    bookings = Booking.query.order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "manage_bookings.html",
        bookings=bookings
    )

@admin.route("/admin/cancel-booking/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    booking = db.session.get(Booking, booking_id)

    if booking is None:
        flash("Booking not found.", "danger")
        return redirect(url_for("admin.manage_bookings"))

    if booking.status != "Booked":
        flash("Only active bookings can be cancelled.", "warning")
        return redirect(url_for("admin.manage_bookings"))

    booking.status = "Cancelled"

    booking.trek.available_slots += 1

    db.session.commit()

    flash("Booking cancelled successfully!", "success")

    return redirect(url_for("admin.manage_bookings"))

@admin.route("/admin/search")
def search():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    query = request.args.get("q", "").strip()

    treks = []
    users = []
    staff = []
    bookings = []

    if query:

        treks = Trek.query.filter(
            or_(
                Trek.name.ilike(f"%{query}%"),
                Trek.location.ilike(f"%{query}%"),
                Trek.public_id.ilike(f"%{query}%")
            )
        ).all()

        users = User.query.filter(
            User.role == "user",
            or_(
                User.name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        ).all()

        staff = User.query.filter(
            User.role == "trek_staff",
            or_(
                User.name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        ).all()

        bookings = Booking.query.filter(
            Booking.public_id.ilike(f"%{query}%")
        ).all()

    return render_template(
        "search_results.html",
        query=query,
        treks=treks,
        users=users,
        staff=staff,
        bookings=bookings
    )

@admin.route("/admin/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    total_bookings = Booking.query.count()

    active_treks = Trek.query.filter_by(
        status="Open"
    ).count()

    completed_treks = Trek.query.filter_by(
        status="Completed"
    ).count()

    cancelled_bookings = Booking.query.filter_by(
        status="Cancelled"
    ).count()

    total_users = User.query.filter_by(
        role="user"
    ).count()

    revenue = db.session.query(
        db.func.sum(Trek.price)
    ).join(
        Booking,
        Booking.trek_id == Trek.id
    ).filter(
        Booking.status.in_(["Booked", "Completed"])
    ).scalar()

    if revenue is None:
        revenue = 0

    most_popular_trek = (
    db.session.query(
        Trek.name,
        func.count(Booking.id).label("booking_count")
    )
    .join(Booking)
    .group_by(Trek.id)
    .order_by(func.count(Booking.id).desc())
    .first()
    )

    most_active_user = (
    db.session.query(
        User.name,
        func.count(Booking.id).label("booking_count")
    )
    .join(Booking)
    .filter(User.role == "user")
    .group_by(User.id)
    .order_by(func.count(Booking.id).desc())
    .first()
    )

    most_active_staff = (
    db.session.query(
        User.name,
        func.count(Trek.id).label("trek_count")
    )
    .join(Trek, Trek.assigned_staff_id == User.id)
    .filter(User.role == "trek_staff")
    .group_by(User.id)
    .order_by(func.count(Trek.id).desc())
    .first()
    )

    booked_count = Booking.query.filter_by(
    status="Booked"
    ).count()

    completed_booking_count = Booking.query.filter_by(
        status="Completed"
    ).count()

    cancelled_booking_count = Booking.query.filter_by(
        status="Cancelled"
    ).count()

    return render_template(
        "reports.html",
        revenue=revenue,
        total_bookings=total_bookings,
        active_treks=active_treks,
        completed_treks=completed_treks,
        cancelled_bookings=cancelled_bookings,
        total_users=total_users,
        most_popular_trek=most_popular_trek,
        most_active_user=most_active_user,
        most_active_staff=most_active_staff,
        booked_count=booked_count,
        completed_booking_count=completed_booking_count,
        cancelled_booking_count=cancelled_booking_count
    )


@admin.route("/admin/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    admin_user = db.session.get(User, session["user_id"])

    if admin_user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template(
        "settings.html",
        admin_user=admin_user
    )

@admin.route("/admin/settings/change-password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    admin_user = db.session.get(User, session["user_id"])

    if admin_user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not current_password or not new_password or not confirm_password:
        flash("All password fields are required.", "danger")
        return redirect(url_for("admin.settings"))

    if not check_password_hash(
        admin_user.password,
        current_password
    ):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("admin.settings"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("admin.settings"))

    if len(new_password) < 6:
        flash("New password must contain at least 6 characters.", "warning")
        return redirect(url_for("admin.settings"))

    admin_user.password = generate_password_hash(new_password)

    db.session.commit()

    flash("Password changed successfully.", "success")

    return redirect(url_for("admin.settings"))