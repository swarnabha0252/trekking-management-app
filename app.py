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

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return f"Welcome {session['name']}! You are logged in as {session['role']}."

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

        new_user = User(name=name,
                        email=email,
                        password=hashed_password,
                        role=role,
                        is_approved=approved)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)