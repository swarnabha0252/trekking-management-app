from flask import Blueprint, render_template, redirect, url_for, session, flash
from models.trek import Trek
from models.booking import Booking
from extensions import db

staff = Blueprint("staff", __name__)

@staff.route("/staff")
def staff_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "trek_staff":
        return "Access Denied", 403

    assigned_treks = Trek.query.filter_by(
    assigned_staff_id=session["user_id"],
    status="Open"
    ).all()
    
    participant_counts = {}

    for trek in assigned_treks:

        participant_counts[trek.id] = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).count()

    participants = {}

    for trek in assigned_treks:

        participants[trek.id] = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

    return render_template(
        "staff_dashboard.html",
        assigned_treks=assigned_treks,
        participant_counts=participant_counts,
        participants=participants
    )

@staff.route("/staff/complete-trek/<int:trek_id>", methods=["POST"])
def complete_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "trek_staff":
        return "Access Denied", 403

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        flash("Trek not found.", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    if trek.assigned_staff_id != session["user_id"]:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    if trek.status == "Completed":
        flash("Trek is already completed.", "warning")
        return redirect(url_for("staff.staff_dashboard"))

    trek.status = "Completed"
    trek.booking_status = "Closed"

    active_bookings = Booking.query.filter_by(
        trek_id=trek.id,
        status="Booked"
    ).all()

    for booking in active_bookings:
        booking.status = "Completed"

    db.session.commit()

    flash("Trek marked as completed successfully!", "success")

    return redirect(url_for("staff.staff_dashboard"))