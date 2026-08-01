from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

staff = Blueprint("staff", __name__)

@staff.route("/staff")
def staff_dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if session["role"] != "trek_staff":
        return "Access Denied", 403
    return render_template("staff_dashboard.html")