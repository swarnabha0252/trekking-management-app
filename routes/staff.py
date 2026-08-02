from flask import Blueprint, render_template, redirect, url_for, session
from models.trek import Trek
from models.booking import Booking

staff = Blueprint("staff", __name__)

@staff.route("/staff")
def staff_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "trek_staff":
        return "Access Denied", 403

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=session["user_id"]
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
