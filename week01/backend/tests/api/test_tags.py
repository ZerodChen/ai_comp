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
async def test_update_tag(client: AsyncClient):
    # Create
    res = await client.post("/api/tags/", json={"name": "Old Name"})
    tag_id = res.json()["id"]
    
    # Update
    response = await client.put(f"/api/tags/{tag_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    
    # Verify update
    get_res = await client.get("/api/tags/")
    assert any(t["name"] == "New Name" for t in get_res.json())

@pytest.mark.anyio
async def test_update_tag_same_name(client: AsyncClient):
    res = await client.post("/api/tags/", json={"name": "Same Name"})
    tag_id = res.json()["id"]
    
    response = await client.put(f"/api/tags/{tag_id}", json={"name": "Same Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Same Name"

@pytest.mark.anyio
async def test_update_tag_not_found(client: AsyncClient):
    response = await client.put("/api/tags/9999", json={"name": "Ghost"})
    assert response.status_code == 404

@pytest.mark.anyio
async def test_update_tag_duplicate_name(client: AsyncClient):
    await client.post("/api/tags/", json={"name": "Taken"})
    res = await client.post("/api/tags/", json={"name": "Change Me"})
    tag_id = res.json()["id"]
    
    response = await client.put(f"/api/tags/{tag_id}", json={"name": "Taken"})
    assert response.status_code == 400

@pytest.mark.anyio
async def test_delete_tag(client: AsyncClient):
    res = await client.post("/api/tags/", json={"name": "To Delete"})
    tag_id = res.json()["id"]
    
    response = await client.delete(f"/api/tags/{tag_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = await client.get(f"/api/tags/")
    data = response.json()
    assert not any(t["id"] == tag_id for t in data)

@pytest.mark.anyio
async def test_delete_tag_not_found(client: AsyncClient):
    response = await client.delete("/api/tags/9999")
    assert response.status_code == 404

@pytest.mark.anyio
async def test_batch_delete_tags(client: AsyncClient):
    t1 = await client.post("/api/tags/", json={"name": "B1"})
    t2 = await client.post("/api/tags/", json={"name": "B2"})
    ids = [t1.json()["id"], t2.json()["id"]]
    
    # FastAPI expects a list directly in the body for List[int]
    response = await client.request("DELETE", "/api/tags/batch", json=ids)
    if response.status_code != 204:
        print(f"Batch Delete Error: {response.json()}")
    assert response.status_code == 204
    
    # Verify
    get_res = await client.get("/api/tags/")
    current_ids = [t["id"] for t in get_res.json()]
    assert not any(i in current_ids for i in ids)
