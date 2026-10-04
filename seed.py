"""Seed the development database with demo data.

Run once before manual testing or taking screenshots:

    python seed.py

Safe to re-run: it stops if volunteers already exist.
"""

from datetime import date, time

from app import create_app
from app.models import Assignment, CrewCall, Performance, Production, Volunteer, db

app = create_app()


def build_performance(production, day, start):
    performance = Performance(production=production, date=day, start_time=start)
    performance.crew_calls.append(CrewCall(role="Box Office", count=2))
    performance.crew_calls.append(CrewCall(role="Front of House", count=2))
    performance.crew_calls.append(CrewCall(role="Bar", count=1))
    return performance


with app.app_context():
    if Volunteer.query.first() is not None:
        print("Database already contains volunteers - nothing to seed.")
        raise SystemExit(0)

    volunteers = [
        Volunteer(name="Marion D'Souza", email="marion@example.com", phone="0400 111 111"),
        Volunteer(name="Priya Raman", email="priya@example.com", phone="0400 222 222"),
        Volunteer(name="Tom Whitfield", email="tom@example.com", phone="0400 333 333"),
        Volunteer(name="Grace Okafor", email="grace@example.com", phone="0400 444 444"),
        Volunteer(name="Ben Nakamura", email="ben@example.com", phone="0400 555 555"),
    ]
    db.session.add_all(volunteers)

    weather_house = Production(title="The Weather House")
    weather_house.performances.append(build_performance(weather_house, date(2026, 10, 16), time(19, 30)))
    weather_house.performances.append(build_performance(weather_house, date(2026, 10, 17), time(14, 0)))

    midsummer = Production(title="A Midsummer Night's Dream")
    midsummer.performances.append(build_performance(midsummer, date(2026, 11, 6), time(19, 30)))

    db.session.add_all([weather_house, midsummer])
    db.session.commit()

    first_show = weather_house.performances[0]
    db.session.add_all(
        [
            Assignment(volunteer=volunteers[0], performance=first_show, role="Box Office", status="confirmed"),
            Assignment(volunteer=volunteers[1], performance=first_show, role="Front of House"),
            Assignment(volunteer=volunteers[2], performance=first_show, role="Bar"),
        ]
    )
    db.session.commit()

    print("Seeded 5 volunteers, 2 productions, 3 performances and 3 assignments.")
