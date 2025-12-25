import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_create_tag(client: AsyncClient):
    response = await client.post("/api/tags/", json={"name": "Test Tag"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Tag"
    assert "id" in data

@pytest.mark.anyio
async def test_read_tags(client: AsyncClient):
    await client.post("/api/tags/", json={"name": "Tag 1"})
    await client.post("/api/tags/", json={"name": "Tag 2"})
    
    response = await client.get("/api/tags/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

@pytest.mark.anyio
async def test_create_duplicate_tag(client: AsyncClient):
    await client.post("/api/tags/", json={"name": "Unique Tag"})
    response = await client.post("/api/tags/", json={"name": "Unique Tag"})
    assert response.status_code == 400

@pytest.mark.anyio
async def test_delete_tag(client: AsyncClient):
    res = await client.post("/api/tags/", json={"name": "To Delete"})
    tag_id = res.json()["id"]
    
    response = await client.delete(f"/api/tags/{tag_id}")
    assert response.status_code == 204
    
    response = await client.get(f"/api/tags/")
    data = response.json()
    assert not any(t["id"] == tag_id for t in data)
