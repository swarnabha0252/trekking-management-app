from flask import Flask, redirect, url_for
from extensions import db
from models.user import User
from models.trek import Trek
from routes.auth import auth
from routes.admin import admin
from routes.user import user
from routes.staff import staff
from models.booking import Booking
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "my-super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"

db.init_app(app)

with app.app_context():
    db.create_all()

    admin_user = User.query.filter_by(role="admin").first()

    if admin_user is None:
        first_admin = User(
            name="admin",
            email="admin@trekking.com",
            password=generate_password_hash("Admin@123"),
            role="admin",
            is_approved=True,
            is_blacklisted=False
        )

        db.session.add(first_admin)
        db.session.commit()

        first_admin.public_id = f"ADM{first_admin.id:04d}"
        db.session.commit()

        print("Admin account created successfully!")

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(staff)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run()