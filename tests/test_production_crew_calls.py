from app.models import Assignment, CrewCall, Performance, Production, db


def test_crew_call_manager_lists_requirements_and_add_form(client, seed):
    response = client.get(f"/productions/{seed['production'].id}/crew-calls")

    assert response.status_code == 200
    assert b"Box Office" in response.data
    assert b"Add requirement" in response.data


def test_create_crew_call_for_existing_performance(client, app, seed):
    production = seed["production"]
    performance = seed["performance"]
    response = client.post(
        f"/productions/{production.id}/performances/{performance.id}/crew-calls/new",
        data={"role": "Lighting Operator", "count": "2"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Lighting Operator" in response.data
    assert b"2 required" in response.data
    assert b"Crew requirement added." in response.data
    with app.app_context():
        call = CrewCall.query.filter_by(
            performance_id=performance.id,
            role="Lighting Operator",
        ).one()
        assert call.count == 2


def test_create_crew_call_rejects_blank_role_and_invalid_count(client, seed):
    production = seed["production"]
    performance = seed["performance"]
    blank_role = client.post(
        f"/productions/{production.id}/performances/{performance.id}/crew-calls/new",
        data={"role": " ", "count": "1"},
    )
    invalid_count = client.post(
        f"/productions/{production.id}/performances/{performance.id}/crew-calls/new",
        data={"role": "Lighting Operator", "count": "0"},
    )

    assert blank_role.status_code == 400
    assert invalid_count.status_code == 400


def test_delete_unassigned_crew_call(client, app, seed):
    production = seed["production"]
    performance = seed["performance"]
    crew_call = performance.crew_calls[0]
    response = client.post(
        f"/productions/{production.id}/performances/{performance.id}/crew-calls/{crew_call.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Crew requirement deleted." in response.data
    with app.app_context():
        assert db.session.get(CrewCall, crew_call.id) is None


def test_delete_crew_call_with_assignments_is_refused(client, app, seed):
    production = seed["production"]
    performance = seed["performance"]
    crew_call = performance.crew_calls[0]
    with app.app_context():
        assignment = Assignment(
            volunteer=seed["volunteer"],
            performance=performance,
            role=crew_call.role,
        )
        db.session.add(assignment)
        db.session.commit()
        assignment_id = assignment.id

    response = client.post(
        f"/productions/{production.id}/performances/{performance.id}/crew-calls/{crew_call.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 409
    assert b"Remove assignments for this role" in response.data
    with app.app_context():
        assert db.session.get(CrewCall, crew_call.id) is not None
        assert db.session.get(Assignment, assignment_id) is not None


def test_crew_call_routes_reject_resources_from_other_performances(client, app, seed):
    with app.app_context():
        other_production = Production(title="Another Production")
        other_performance = Performance(
            production=other_production,
            date=seed["performance"].date,
            start_time=seed["performance"].start_time,
        )
        db.session.add(other_production)
        db.session.commit()
        other_production_id = other_production.id
        other_performance_id = other_performance.id

    response = client.post(
        f"/productions/{seed['production'].id}/performances/{other_performance_id}/crew-calls/new",
        data={"role": "Usher", "count": "1"},
    )

    assert response.status_code == 404
