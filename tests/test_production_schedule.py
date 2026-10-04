from datetime import date, time

from app.models import Performance, Production, db


def test_production_schedule_lists_performance_and_edit_link(client, seed):
    response = client.get(f"/productions/{seed['production'].id}/schedule")

    assert response.status_code == 200
    assert b"04 Sep 2026" in response.data
    assert b"19:30" in response.data
    assert b"Edit date and time" in response.data


def test_edit_performance_schedule_updates_date_and_time(client, app, seed):
    production = seed["production"]
    performance = seed["performance"]
    response = client.post(
        f"/productions/{production.id}/performances/{performance.id}/edit-schedule",
        data={"date": "2026-09-06", "start_time": "20:00"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Performance schedule updated." in response.data
    assert b"06 Sep 2026" in response.data
    assert b"20:00" in response.data
    with app.app_context():
        saved = db.session.get(Performance, performance.id)
        assert saved.date == date(2026, 9, 6)
        assert saved.start_time == time(20, 0)


def test_edit_performance_schedule_rejects_invalid_date_without_saving(client, app, seed):
    production = seed["production"]
    performance = seed["performance"]
    response = client.post(
        f"/productions/{production.id}/performances/{performance.id}/edit-schedule",
        data={"date": "not-a-date", "start_time": "20:00"},
    )

    assert response.status_code == 400
    assert b"Date and start time are required" in response.data
    with app.app_context():
        saved = db.session.get(Performance, performance.id)
        assert saved.date == date(2026, 9, 4)
        assert saved.start_time == time(19, 30)


def test_edit_schedule_rejects_performance_from_another_production(client, app, seed):
    with app.app_context():
        other_production = Production(title="Another Production")
        db.session.add(other_production)
        db.session.commit()
        other_id = other_production.id

    response = client.get(
        f"/productions/{other_id}/performances/{seed['performance'].id}/edit-schedule"
    )

    assert response.status_code == 404
