from datetime import date, time

from app.models import Assignment, Performance, Volunteer, db


def test_assign_volunteer(client, seed):
    response = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Box Office" in response.data


def test_new_assignment_starts_unconfirmed(app, seed):
    with app.app_context():
        assignment = Assignment(
            volunteer=seed["volunteer"],
            performance=seed["performance"],
            role="Usher",
        )
        db.session.add(assignment)
        db.session.commit()
        assert assignment.status == "unconfirmed"


def test_second_role_same_performance_is_refused(client, seed):
    first = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    assert first.status_code == 302

    second = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Bar",
        },
    )
    assert second.status_code == 409
    assert b"Refused" in second.data


def test_same_volunteer_different_performance_is_allowed(client, app, seed):
    with app.app_context():
        other = Performance(
            production=seed["production"],
            date=date(2026, 9, 12),
            start_time=time(19, 30),
        )
        db.session.add(other)
        db.session.commit()
        other_id = other.id

    first = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    assert first.status_code == 302

    second = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": other_id,
            "role": "Bar",
        },
        follow_redirects=True,
    )
    assert second.status_code == 200
    assert b"Bar" in second.data


def test_delete_assignment_leaves_position_open(client, app, seed):
    first = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    assert first.status_code == 302

    with app.app_context():
        assignment = Assignment.query.first()
        assert assignment is not None
        assignment_id = assignment.id

    response = client.post(f"/assignments/{assignment_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"No assignments yet." in response.data


def test_filter_assignments_by_performance(client, seed):
    client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )

    matching = client.get(f"/assignments?performance_id={seed['performance'].id}")
    assert matching.status_code == 200
    assert b"Box Office" in matching.data

    other = client.get("/assignments?performance_id=999999")
    assert other.status_code == 200
    assert b"Box Office" not in other.data


def test_toggle_status_confirms_assignment(client, app, seed):
    client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    with app.app_context():
        assignment_id = Assignment.query.first().id

    response = client.post(
        f"/assignments/{assignment_id}/toggle-status", follow_redirects=True
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Assignment, assignment_id).status == "confirmed"


def test_roster_groups_assignments_by_performance(client, seed):
    client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )

    response = client.get("/assignments/roster")
    assert response.status_code == 200
    assert b"Box Office" in response.data
    assert b"No one assigned yet." not in response.data


def test_edit_assignment_updates_role(client, app, seed):
    client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    with app.app_context():
        assignment_id = Assignment.query.first().id

    response = client.post(
        f"/assignments/{assignment_id}/edit",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Front of House",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Front of House" in response.data
    with app.app_context():
        assert db.session.get(Assignment, assignment_id).role == "Front of House"


def test_edit_cannot_move_into_a_clashing_performance(client, app, seed):
    with app.app_context():
        other = Performance(
            production=seed["production"],
            date=date(2026, 9, 12),
            start_time=time(19, 30),
        )
        db.session.add(other)
        db.session.commit()
        other_id = other.id

    client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": other_id,
            "role": "Bar",
        },
    )
    with app.app_context():
        movable_id = Assignment.query.filter_by(performance_id=other_id).first().id

    response = client.post(
        f"/assignments/{movable_id}/edit",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Bar",
        },
    )
    assert response.status_code == 409
    assert b"Refused" in response.data


def test_inactive_volunteer_cannot_be_assigned(client, app, seed):
    with app.app_context():
        volunteer = db.session.get(Volunteer, seed["volunteer"].id)
        volunteer.is_active = False
        db.session.commit()

    response = client.post(
        "/assignments/new",
        data={
            "volunteer_id": seed["volunteer"].id,
            "performance_id": seed["performance"].id,
            "role": "Box Office",
        },
    )
    assert response.status_code == 400
    assert b"active volunteer" in response.data
