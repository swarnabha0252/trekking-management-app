from datetime import datetime
from extensions import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)

    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    assigned_staff = db.relationship(
        "User",
        foreign_keys=[assigned_staff_id],
        backref="assigned_treks"
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )
    
    booking_status = db.Column(
    db.String(20),
    nullable=False,
    default="Closed"
    )

    rating = db.Column(
    db.Float,
    nullable=False,
    default=0.0
    )
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )