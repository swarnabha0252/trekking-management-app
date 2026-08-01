from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "my-super-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///trekking.db"
db.init_app(app)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()

    if admin is None:
        first_admin = User(
            name="Admin",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            role="admin",
            is_approved=True,
            is_blacklisted=False
        )

        db.session.add(first_admin)
        db.session.commit()

        first_admin.public_id = f"ADM{first_admin.id:04d}"
        db.session.commit()

        print("Admin account created successfully!")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] == "admin":
        return redirect(url_for("admin_dashboard"))
    elif session["role"] == "trek_staff":
        return redirect(url_for("staff_dashboard"))
    elif session["role"] == "user":
        return redirect(url_for("user_dashboard"))

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
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

@app.route("/admin")
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

@app.route("/admin/staff")
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

@app.route("/admin/staff/approve/<int:user_id>")
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

@app.route("/admin/staff/reject/<int:user_id>")
def reject_staff(user_id):
    return "Reject functionality coming soon."

@app.route("/staff")
def staff_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "trek_staff":
        return "Access Denied", 403
    return render_template("staff_dashboard.html")


@app.route("/user")
def user_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "user":
        return "Access Denied", 403
    return render_template("user_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)