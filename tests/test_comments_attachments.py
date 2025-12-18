def test_comments_and_attachments_lifecycle(client):
    # create project and task
    r = client.post("/projects/", json={"name": "CProj", "budget": 10, "is_active": True})
    assert r.status_code == 200
    proj = r.json()
    r = client.post("/tasks/", json={"name": "CTask", "project_id": proj["id"], "status": "open", "priority": "low", "time_estimation": 1})
    assert r.status_code == 200
    task = r.json()

    # create comment
    r = client.post("/comments/", json={"task_id": task["id"], "author": "bob", "message": "hello", "rating": 5})
    if r.status_code != 200:
        print('COMMENT ERROR', r.status_code, r.text)
    assert r.status_code == 200
    comment = r.json()
    assert comment["author"] == "bob"

    # create attachment
    r = client.post("/attachments/", json={"comment_id": comment["id"], "file_name": "f.txt", "type": "txt", "size_kb": 4})
    assert r.status_code == 200
    att = r.json()
    assert att["file_name"] == "f.txt"

    # list comments and attachments
    r = client.get("/comments/")
    assert r.status_code == 200
    assert any(c["id"] == comment["id"] for c in r.json())

    r = client.get("/attachments/")
    assert r.status_code == 200
    assert any(a["id"] == att["id"] for a in r.json())

    # update comment
    r = client.put(f"/comments/{comment['id']}", json={"message": "edited"})
    assert r.status_code == 200
    assert r.json()["message"] == "edited"

    # delete attachment
    r = client.delete(f"/attachments/{att['id']}")
    assert r.status_code == 200
