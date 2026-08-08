from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from extensions import db
from models.trek import Trek
from models.booking import Booking
from models.user import User

user = Blueprint("user", __name__)


@user.route("/user")
def user_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "user":
        return "Access Denied", 403

    booked_trek_ids = db.session.query(
        Booking.trek_id
    ).filter(
        Booking.user_id == session["user_id"],
        Booking.status == "Booked"
    ).subquery()

    treks = Trek.query.filter(
        Trek.status == "Open",
        Trek.booking_status == "Open",
        Trek.available_slots > 0,
        ~Trek.id.in_(booked_trek_ids)
    ).all()

    return render_template(
        "user_dashboard.html",
        treks=treks
    )


@user.route("/user/book/<int:trek_id>")
def book_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "user":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    if not trek:
        flash("Trek not found.", "danger")
        return redirect(url_for("user.user_dashboard"))

    if trek.status != "Open":
        flash("This trek is not available.", "warning")
        return redirect(url_for("user.user_dashboard"))

    if trek.booking_status != "Open":
        flash("Bookings for this trek are closed.", "warning")
        return redirect(url_for("user.user_dashboard"))

    if trek.available_slots <= 0:
        flash("No slots available.", "danger")
        return redirect(url_for("user.user_dashboard"))

    existing_booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing_booking:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.my_bookings"))

    booking_count = Booking.query.count() + 1

    public_id = f"BK{booking_count:04d}"

    new_booking = Booking(
        public_id=public_id,
        user_id=session["user_id"],
        trek_id=trek.id,
        status="Booked"
    )

    db.session.add(new_booking)

    trek.available_slots -= 1

    if trek.available_slots == 0:
        trek.booking_status = "Closed"

    db.session.commit()

    flash("Trek booked successfully!", "success")

    return redirect(url_for("user.my_bookings"))


@user.route("/user/my-bookings")
def my_bookings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "user":
        return "Access Denied", 403

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )


@user.route("/user/cancel-booking/<int:booking_id>")
def cancel_booking(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "user":
        return "Access Denied", 403

    booking = db.session.get(Booking, booking_id)

    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("user.my_bookings"))

    if booking.user_id != session["user_id"]:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("user.my_bookings"))

    if booking.status != "Booked":
        flash("Booking has already been cancelled.", "warning")
        return redirect(url_for("user.my_bookings"))

    booking.status = "Cancelled"

    trek = booking.trek

    trek.available_slots += 1

    if trek.status == "Open" and trek.booking_status == "Closed":
        trek.booking_status = "Open"

    db.session.commit()

    flash("Booking cancelled successfully.", "success")

    return redirect(url_for("user.my_bookings"))


@user.route("/user/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "user":
        return "Access Denied", 403

    user_account = db.session.get(User, session["user_id"])

    if not user_account:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        if not name:
            flash("Name cannot be empty.", "danger")
            return redirect(url_for("user.profile"))

        if not email:
            flash("Email cannot be empty.", "danger")
            return redirect(url_for("user.profile"))

        existing_user = User.query.filter(
            User.email == email,
            User.id != user_account.id
        ).first()

        if existing_user:
            flash("This email address is already registered.", "danger")
            return redirect(url_for("user.profile"))

        user_account.name = name
        user_account.email = email
        user_account.phone = phone if phone else None

        session["name"] = name

        db.session.commit()

        flash("Profile updated successfully.", "success")

        return redirect(url_for("user.profile"))

    return render_template(
        "profile.html",
        user=user_account
    )