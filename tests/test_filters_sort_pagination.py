def test_project_filters_sort_pagination(client):
    # create multiple projects
    client.post("/projects/", json={"name": "A", "budget": 10, "is_active": True})
    client.post("/projects/", json={"name": "B", "budget": 50, "is_active": False})
    client.post("/projects/", json={"name": "C", "budget": 30, "is_active": True})

    # filter by name substring
    r = client.get("/projects/?name=B")
    assert r.status_code == 200
    arr = r.json()
    assert len(arr) == 1 and arr[0]["name"] == "B"

    # budget range
    r = client.get("/projects/?min_budget=20&max_budget=40")
    assert r.status_code == 200
    arr = r.json()
    assert all(20 <= float(p["budget"] or 0) <= 40 for p in arr)

    # sort by budget desc
    r = client.get("/projects/?sort_by=budget&sort_dir=desc")
    assert r.status_code == 200
    arr = r.json()
    budgets = [float(p["budget"] or 0) for p in arr]
    assert budgets == sorted(budgets, reverse=True)

    # pagination
    r = client.get("/projects/?limit=1&offset=1")
    assert r.status_code == 200
    assert len(r.json()) <= 1
