from flask import Blueprint, render_template, redirect, url_for, session
from extensions import db
from models.user import User
from models.trek import Trek

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied", 403
    
    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="trek_staff").count()
    total_treks = 0
    total_bookings = 0
    
    return render_template("admin_dashboard.html", total_users=total_users, total_staff=total_staff, total_treks=total_treks, total_bookings=total_bookings)

@admin.route("/admin/staff")
def manage_staff():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    pending_staff = User.query.filter_by(
    role="trek_staff",
    is_approved=False
    ).all()
    return render_template("manage_staff.html", pending_staff=pending_staff)

@admin.route("/admin/staff/approve/<int:user_id>")
def approve_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

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

    return redirect(url_for("manage_staff"))

@admin.route("/admin/staff/reject/<int:user_id>")
def reject_staff(user_id):
    return "Reject functionality coming soon."