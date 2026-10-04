from datetime import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": False})


class Volunteer(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    assignments = db.relationship("Assignment", back_populates="volunteer")


class Production(db.Model):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    performances = db.relationship(
        "Performance",
        back_populates="production",
        cascade="all, delete-orphan",
        order_by="Performance.date, Performance.start_time",
    )


class Performance(db.Model):
    __tablename__ = "performances"

    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    # Nullable so existing databases can be upgraded without inventing a duration.
    duration_minutes = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    production = db.relationship("Production", back_populates="performances")
    crew_calls = db.relationship("CrewCall", back_populates="performance", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="performance", cascade="all, delete-orphan")

    @property
    def starts_at(self):
        return datetime.combine(self.date, self.start_time)

    @property
    def ends_at(self):
        if self.duration_minutes is None or self.duration_minutes <= 0:
            return None
        return self.starts_at + timedelta(minutes=self.duration_minutes)

    @property
    def time_range(self):
        if self.ends_at is None:
            return None
        days_later = (self.ends_at.date() - self.date).days
        end_suffix = f" (+{days_later} day{'s' if days_later != 1 else ''})" if days_later else ""
        return f"{self.start_time.strftime('%H:%M')} - {self.ends_at.strftime('%H:%M')}{end_suffix}"


class CrewCall(db.Model):
    __tablename__ = "crew_calls"

    id = db.Column(db.Integer, primary_key=True)
    performance_id = db.Column(db.Integer, db.ForeignKey("performances.id"), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=1)

    performance = db.relationship("Performance", back_populates="crew_calls")


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    performance_id = db.Column(db.Integer, db.ForeignKey("performances.id"), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="unconfirmed")

    performance = db.relationship("Performance", back_populates="assignments")
    volunteer = db.relationship("Volunteer", back_populates="assignments")

    __table_args__ = (
        db.UniqueConstraint("volunteer_id", "performance_id", name="uq_assignment_volunteer_performance"),
    )


def find_assignment(volunteer_id, performance_id):
    return Assignment.query.filter_by(
        volunteer_id=volunteer_id, performance_id=performance_id
    ).first()
