from app.models import Assignment, Volunteer, db


def test_create_volunteer(client):
    response = client.post(
        "/volunteers/new",
        data={"name": "Kylie Toomey", "phone": "0409 226 731"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Kylie Toomey" in response.data


def test_volunteer_requires_name(client):
    response = client.post("/volunteers/new", data={"name": ""})
    assert response.status_code == 400


def test_volunteer_persists(client, app):
    client.post("/volunteers/new", data={"name": "Vera Sokolova"})
    with app.app_context():
        assert Volunteer.query.count() == 1


def test_deactivate_keeps_assignments(client, app, seed):
    with app.app_context():
        assignment = Assignment(
            volunteer=seed["volunteer"],
            performance=seed["performance"],
            role="Box Office",
        )
        db.session.add(assignment)
        db.session.commit()
        assignment_id = assignment.id

    client.post(f"/volunteers/{seed['volunteer'].id}/toggle")

    with app.app_context():
        assert db.session.get(Assignment, assignment_id) is not None


def test_search_volunteer(client):
    client.post("/volunteers/new", data={"name": "Kylie Toomey"})
    client.post("/volunteers/new", data={"name": "Vera Sokolova"})
    response = client.get("/volunteers?q=Kylie")
    assert b"Kylie Toomey" in response.data
    assert b"Vera Sokolova" not in response.data


def test_filter_volunteer_by_status(client, app):
    client.post("/volunteers/new", data={"name": "Active Person"})
    client.post("/volunteers/new", data={"name": "Inactive Person"})
    with app.app_context():
        inactive = Volunteer.query.filter_by(name="Inactive Person").first()
        inactive.is_active = False
        db.session.commit()
    
    response = client.get("/volunteers?status=active")
    assert b"Active Person" in response.data
    assert b"Inactive Person" not in response.data