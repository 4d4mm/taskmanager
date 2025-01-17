from fastapi.testclient import TestClient


def test_create_task(client: TestClient):
    response = client.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data
    assert "created_at" in data


def test_post_missing_title(client: TestClient):
    response = client.post("/tasks", json={"description": "Test description", "completed": True})
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]


def test_post_invalid_completed_type(client: TestClient):
    response = client.post(
        "/tasks", json={"title": "Test Title", "description": "Test description", "completed": 123123}
    )
    assert response.status_code == 422
    assert "completed" in response.json()["detail"][0]["loc"]


def test_get_tasks(client: TestClient):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_non_existent_task(client: TestClient):
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_nonexistent_task(client: TestClient):
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["completed"] == True


def test_put_missing_title(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"description": "Test description", "completed": True})
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]


def test_put_invalid_completed_type(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    response = client.put(
        f"/tasks/{task_id}", json={"title": "Test Title", "description": "Test description", "completed": 123123}
    )
    assert response.status_code == 422
    assert "completed" in response.json()["detail"][0]["loc"]


def test_put_malformed_request_body(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={})
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]


def test_update_non_existent_task(client: TestClient):
    updated_task = {"title": "Updated Title", "description": "Updated Description", "completed": True}
    response = client.put("/tasks/9999", json=updated_task)
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_patch_task(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] == True


def test_patch_invalid_completed_type(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}", json={"title": "Test Title", "description": "Test description", "completed": 123123}
    )
    assert response.status_code == 422
    assert "completed" in response.json()["detail"][0]["loc"]


def test_patch_non_existent_task(client: TestClient):
    partial_update = {"title": "Patched Title"}
    response = client.patch("/tasks/9999", json=partial_update)
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client: TestClient):
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_task(client: TestClient):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_filter_tasks_by_completion(client: TestClient):
    client.post("/tasks", json={"title": "Task 1", "completed": True})
    client.post("/tasks", json={"title": "Task 2", "completed": False})

    response = client.get("/tasks?completed=true")
    assert response.status_code == 200
    tasks = response.json()
    assert all(task["completed"] for task in tasks)

    response = client.get("/tasks?completed=false")
    assert response.status_code == 200
    tasks = response.json()
    assert all(not task["completed"] for task in tasks)
