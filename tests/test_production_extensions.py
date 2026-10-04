from datetime import date, time

from app.models import Assignment, CrewCall, Performance, Production, db


def test_management_page_shows_overlap_and_duration(client, seed, app):
    with app.app_context():
        second = Performance(
            production_id=seed["production"].id,
            date=date(2026, 9, 4),
            start_time=time(20, 0),
            duration_minutes=60,
        )
        seed["performance"].duration_minutes = 90
        db.session.add(second)
        db.session.commit()
        production_id = seed["production"].id

    response = client.get(f"/productions/{production_id}/management")
    assert response.status_code == 200
    assert b"19:30 - 21:00" in response.data
    assert b"multiple performances are scheduled at the same time" in response.data


def test_new_performance_rejects_zero_duration_and_nonpositive_headcount(client, seed):
    response = client.post(
        f"/productions/{seed['production'].id}/performances/new-enhanced",
        data={"date": "2026-09-04", "start_time": "19:00", "duration_minutes": "0", "role": "Sound", "count": "1"},
    )
    assert response.status_code == 400
    assert b"Duration must be greater than 0 minutes" in response.data

    response = client.post(
        f"/productions/{seed['production'].id}/performances/new-enhanced",
        data={"date": "2026-09-04", "start_time": "19:00", "duration_minutes": "60", "role": "Sound", "count": "0"},
    )
    assert response.status_code == 400
    assert b"Headcount for each crew-call role must be greater than 0" in response.data

    response = client.post(
        f"/productions/{seed['production'].id}/performances/new-enhanced",
        data={"date": "2026-09-04", "start_time": "19:00", "duration_minutes": "60", "role": "Sound", "count": "not-a-number"},
    )
    assert response.status_code == 400
    assert b"Enter a valid whole number for the crew-call headcount" in response.data


def test_new_performance_saves_duration_and_multiple_crew_roles(client, seed, app):
    response = client.post(
        f"/productions/{seed['production'].id}/performances/new-enhanced",
        data={
            "date": "2026-09-05",
            "start_time": "19:00",
            "duration_minutes": "75",
            "role": ["Sound Operator", "Lighting Operator"],
            "count": ["2", "1"],
        },
    )
    assert response.status_code == 302
    with app.app_context():
        performance = Performance.query.filter_by(date=date(2026, 9, 5)).one()
        assert performance.duration_minutes == 75
        assert {(row.role, row.count) for row in performance.crew_calls} == {
            ("Sound Operator", 2),
            ("Lighting Operator", 1),
        }


def test_performance_delete_requires_explicit_confirmation(client, seed, app):
    url = f"/productions/{seed['production'].id}/performances/{seed['performance'].id}/delete-enhanced"
    response = client.post(url, data={"confirmed": "no"})
    assert response.status_code == 400
    with app.app_context():
        assert db.session.get(Performance, seed["performance"].id) is not None


def test_confirmed_performance_delete_removes_its_assignments(client, seed, app):
    with app.app_context():
        assignment = Assignment(
            performance_id=seed["performance"].id,
            volunteer_id=seed["volunteer"].id,
            role="Box Office",
        )
        db.session.add(assignment)
        db.session.commit()
        production_id = seed["production"].id
        performance_id = seed["performance"].id

    response = client.post(
        f"/productions/{production_id}/performances/{performance_id}/delete-enhanced",
        data={"confirmed": "yes"},
    )
    assert response.status_code == 302
    with app.app_context():
        assert db.session.get(Performance, performance_id) is None
        assert Assignment.query.filter_by(performance_id=performance_id).count() == 0


def test_crew_call_edit_and_delete_confirmation(client, seed, app):
    with app.app_context():
        crew_call_id = seed["performance"].crew_calls[0].id
        production_id = seed["production"].id
        performance_id = seed["performance"].id

    edit_url = (
        f"/productions/{production_id}/performances/{performance_id}/"
        f"crew-calls/{crew_call_id}/edit-enhanced"
    )
    response = client.post(edit_url, data={"role": "Sound Operator", "count": "3"})
    assert response.status_code == 302
    with app.app_context():
        crew_call = db.session.get(CrewCall, crew_call_id)
        assert (crew_call.role, crew_call.count) == ("Sound Operator", 3)

    delete_url = (
        f"/productions/{production_id}/performances/{performance_id}/"
        f"crew-calls/{crew_call_id}/delete-enhanced"
    )
    response = client.post(delete_url, data={"confirmed": "no"})
    assert response.status_code == 400
    response = client.post(delete_url, data={"confirmed": "yes"})
    assert response.status_code == 302
    with app.app_context():
        assert db.session.get(CrewCall, crew_call_id) is None


def test_production_delete_requires_confirmation_and_deletes_when_confirmed(client, seed, app):
    production_id = seed["production"].id
    url = f"/productions/{production_id}/delete-enhanced"
    response = client.post(url, data={"confirmed": "no"})
    assert response.status_code == 400
    response = client.post(url, data={"confirmed": "yes"})
    assert response.status_code == 302
    with app.app_context():
        assert db.session.get(Production, production_id) is None
