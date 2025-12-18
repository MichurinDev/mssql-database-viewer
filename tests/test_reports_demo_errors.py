def test_reports_and_demo_endpoints(client):
    # ensure at least one project and task exist
    r = client.post("/projects/", json={"name": "RProj", "budget": 5, "is_active": True})
    p = r.json()
    client.post("/tasks/", json={"name": "RT", "project_id": p["id"], "status": "done", "priority": "high", "time_estimation": 2})

    r = client.get("/reports/project_task_count")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    r = client.get("/reports/tasks_with_project")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    r = client.get("/demo/sets")
    assert r.status_code == 200

    r = client.get("/demo/functions")
    assert r.status_code == 200


def test_error_cases(client):
    # nonexistent project/task
    r = client.get("/projects/999999")
    assert r.status_code == 404
    r = client.get("/tasks/999999")
    assert r.status_code == 404
