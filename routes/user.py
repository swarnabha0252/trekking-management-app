from flask import Blueprint, render_template, redirect, url_for, session, flash
from extensions import db
from models.trek import Trek
from models.booking import Booking

user = Blueprint("user", __name__)


@user.route("/user")
def user_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "user":
        return "Access Denied", 403

    treks = Trek.query.filter_by(
        status="Open",
        booking_status="Open"
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
        return redirect(url_for("user.user_dashboard"))

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