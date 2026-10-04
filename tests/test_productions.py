def test_create_production(client):
    response = client.post(
        "/productions/new",
        data={"title": "Salt on the Wind"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Salt on the Wind" in response.data


def test_create_performance_with_crew_call(client, seed):
    response = client.post(
        f"/productions/{seed['production'].id}/performances/new",
        data={
            "date": "2026-09-05",
            "start_time": "14:00",
            "role": ["Lighting Op", "Usher"],
            "count": ["1", "2"],
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Lighting Op" in response.data
    assert b"Usher x2" in response.data


def test_performances_listed_in_order(client, app, seed):
    from datetime import date, time

    from app.models import Performance, db

    with app.app_context():
        later = Performance(
            production=seed["production"],
            date=date(2026, 9, 12),
            start_time=time(19, 30),
        )
        db.session.add(later)
        db.session.commit()
    response = client.get(f"/productions/{seed['production'].id}")
    assert response.status_code == 200
    assert response.data.index(b"04 Sep") < response.data.index(b"12 Sep")


from app.models import CrewCall, Performance, Production, db


# Non-destructive A2 extension: existing tests above remain unchanged.
def test_manage_production_lists_existing_crew_calls(client, seed):
    response = client.get(f"/productions/{seed['production'].id}/manage")
    assert response.status_code == 200
    assert b"Manage The Weather House" in response.data
    assert b"Box Office: 1 required" in response.data


def test_edit_production_title_prefills_and_persists(client, app, seed):
    production = seed["production"]
    page = client.get(f"/productions/{production.id}/edit-title")
    assert page.status_code == 200
    assert production.title.encode() in page.data

    response = client.post(
        f"/productions/{production.id}/edit-title",
        data={"title": "The Weather House Revised"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"The Weather House Revised" in response.data
    with app.app_context():
        assert db.session.get(Production, production.id).title == "The Weather House Revised"


def test_edit_production_title_rejects_blank_value(client, seed):
    response = client.post(
        f"/productions/{seed['production'].id}/edit-title", data={"title": ""}
    )
    assert response.status_code == 400
    assert b"Title is required" in response.data


def test_edit_crew_call_updates_required_count(client, app, seed):
    performance = seed["performance"]
    crew_call = performance.crew_calls[0]
    response = client.post(
        f"/productions/{seed['production'].id}/performances/{performance.id}/crew-calls/{crew_call.id}/edit",
        data={"role": "Box Office", "count": "2"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Box Office: 2 required" in response.data
    with app.app_context():
        assert db.session.get(CrewCall, crew_call.id).count == 2


def test_edit_crew_call_rejects_non_positive_count(client, app, seed):
    performance = seed["performance"]
    crew_call = performance.crew_calls[0]
    response = client.post(
        f"/productions/{seed['production'].id}/performances/{performance.id}/crew-calls/{crew_call.id}/edit",
        data={"role": "Box Office", "count": "0"},
    )
    assert response.status_code == 400
    assert b"at least 1" in response.data
    with app.app_context():
        assert db.session.get(CrewCall, crew_call.id).count == 1


def test_delete_performance_cascades_its_assignments_only(client, app, seed):
    from app.models import Assignment

    performance = seed["performance"]
    with app.app_context():
        assignment = Assignment(
            volunteer=seed["volunteer"], performance=performance, role="Box Office"
        )
        db.session.add(assignment)
        db.session.commit()
        assignment_id = assignment.id

    response = client.post(
        f"/productions/{seed['production'].id}/performances/{performance.id}/delete",
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Performance, performance.id) is None
        assert db.session.get(Assignment, assignment_id) is None
