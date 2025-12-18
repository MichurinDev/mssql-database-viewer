def test_create_and_list_project(client):
    # create project
    resp = client.post("/projects/", json={"name": "TestProj", "budget": 1234.5, "is_active": True})
    assert resp.status_code == 200
    proj = resp.json()
    assert proj["name"] == "TestProj"

    # list projects
    resp = client.get("/projects/")
    assert resp.status_code == 200
    arr = resp.json()
    assert any(p["name"] == "TestProj" for p in arr)


def test_project_aggregate(client):
    resp = client.get("/projects/aggregate")
    assert resp.status_code == 200
    j = resp.json()
    assert "count" in j and "sum_budget" in j


def test_create_task_and_relations(client):
    # create project
    resp = client.post("/projects/", json={"name": "P2", "budget": 50.0, "is_active": True})
    assert resp.status_code == 200
    proj = resp.json()

    # create task linked to project
    resp = client.post("/tasks/", json={"name": "T1", "project_id": proj["id"], "status": "open", "priority": "low", "time_estimation": 3})
    assert resp.status_code == 200
    task = resp.json()
    assert task["name"] == "T1"

    # get task
    resp = client.get(f"/tasks/{task['id']}")
    assert resp.status_code == 200

    # tasks aggregate
    resp = client.get("/tasks/aggregate")
    assert resp.status_code == 200
    j = resp.json()
    assert "count" in j and "avg_time" in j
