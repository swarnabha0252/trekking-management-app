from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] == "admin":
        return redirect(url_for("admin_dashboard"))
    elif session["role"] == "trek_staff":
        return redirect(url_for("staff_dashboard"))
    elif session["role"] == "user":
        return redirect(url_for("user_dashboard"))

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            if user.is_blacklisted:
                return "Your account has been blacklisted. Please contact support."

            if not user.is_approved:
                return "Your account is not approved yet. Please wait for approval."

            session["user_id"] = user.id
            session["role"] = user.role
            session["name"] = user.name

            return redirect(url_for("dashboard"))

        return "Invalid email or password."

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User with this email already exists."
        
        if role == "user":
            approved = True
        else:
            approved = False

        if role == "admin":
            admin_count = User.query.filter_by(role="admin").count() + 1
            public_id = f"ADM{admin_count:04d}"
        elif role == "trek_staff":
            staff_count = User.query.filter_by(role="trek_staff").count() + 1
            public_id = f"TS{staff_count:04d}"
        else:
            user_count = User.query.filter_by(role="user").count() + 1
            public_id = f"U{user_count:04d}"

        new_user = User(name=name,
                                email=email,
                                password=hashed_password,
                                role=role,
                                is_approved=approved,
                                public_id=public_id)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")