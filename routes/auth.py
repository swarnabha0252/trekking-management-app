from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] == "admin":

        return redirect(
            url_for("admin.admin_dashboard")
        )

    elif session["role"] == "trek_staff":

        return redirect(
            url_for("staff.staff_dashboard")
        )

    elif session["role"] == "user":

        return redirect(
            url_for("user.user_dashboard")
        )

    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            # Check blocked status first so the user
            # receives the correct notification.

            if user.is_blacklisted:

                flash(
                    "Your account has been blocked by the administrator. Kindly contact the administrator for further assistance.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            # Check password after checking account status.

            if not check_password_hash(
                user.password,
                password
            ):

                flash(
                    "Invalid email or password.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            # Check whether the account has been approved.

            if not user.is_approved:

                flash(
                    "Your account is not approved yet. Please wait for approval.",
                    "warning"
                )

                return redirect(
                    url_for("auth.login")
                )

            # Create session.

            session["user_id"] = user.id
            session["role"] = user.role
            session["name"] = user.name

            return redirect(
                url_for("auth.dashboard")
            )

        # User with this email does not exist.

        flash(
            "Invalid email or password.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "login.html"
    )


@auth.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        hashed_password = generate_password_hash(
            password
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "User with this email already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # Normal users are automatically approved.
        # Admin and Trek Staff accounts require approval.

        if role == "user":

            approved = True

        else:

            approved = False

        # Generate public ID.

        if role == "admin":

            admin_count = User.query.filter_by(
                role="admin"
            ).count() + 1

            public_id = f"ADM{admin_count:04d}"

        elif role == "trek_staff":

            staff_count = User.query.filter_by(
                role="trek_staff"
            ).count() + 1

            public_id = f"TS{staff_count:04d}"

        else:

            user_count = User.query.filter_by(
                role="user"
            ).count() + 1

            public_id = f"U{user_count:04d}"

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            is_approved=approved,
            public_id=public_id
        )

        db.session.add(
            new_user
        )

        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )
