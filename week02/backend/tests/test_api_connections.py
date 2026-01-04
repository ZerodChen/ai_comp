def test_create_connection(client):
    response = client.post(
        "/api/v1/connections/",
        json={"name": "Test DB", "db_type": "sqlite", "connection_url": "sqlite:///:memory:"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test DB"
    assert "id" in data

def test_list_connections(client):
    client.post(
        "/api/v1/connections/",
        json={"name": "Test DB 1", "db_type": "sqlite", "connection_url": "sqlite:///:memory:"}
    )
    response = client.get("/api/v1/connections/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
