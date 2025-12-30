import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_create_ticket(client: AsyncClient):
    response = await client.post("/api/tickets/", json={"title": "New Ticket", "description": "Desc"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Ticket"
    assert data["description"] == "Desc"

@pytest.mark.anyio
async def test_create_ticket_with_tags(client: AsyncClient):
    # Create tag first
    tag_res = await client.post("/api/tags/", json={"name": "Bug"})
    tag_id = tag_res.json()["id"]
    
    response = await client.post("/api/tickets/", json={
        "title": "Bug Ticket",
        "tags": [tag_id]
    })
    assert response.status_code == 201
    data = response.json()
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "Bug"

@pytest.mark.anyio
async def test_get_ticket(client: AsyncClient):
    create = await client.post("/api/tickets/", json={"title": "Get Me"})
    tid = create.json()["id"]
    
    response = await client.get(f"/api/tickets/{tid}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"

@pytest.mark.anyio
async def test_get_ticket_not_found(client: AsyncClient):
    response = await client.get("/api/tickets/9999")
    assert response.status_code == 404

@pytest.mark.anyio
async def test_update_ticket(client: AsyncClient):
    create = await client.post("/api/tickets/", json={"title": "Original"})
    tid = create.json()["id"]
    
    # Create a tag to attach
    tag = await client.post("/api/tags/", json={"name": "UpdateTag"})
    tag_id = tag.json()["id"]
    
    response = await client.put(f"/api/tickets/{tid}", json={
        "title": "Updated",
        "description": "New Desc",
        "tags": [tag_id]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["tags"][0]["id"] == tag_id

@pytest.mark.anyio
async def test_update_ticket_partial(client: AsyncClient):
    create = await client.post("/api/tickets/", json={"title": "Part", "description": "Desc"})
    tid = create.json()["id"]
    
    # Update only title
    response = await client.put(f"/api/tickets/{tid}", json={"title": "Part Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Part Updated"
    assert data["description"] == "Desc"
    
    # Update only description
    response = await client.put(f"/api/tickets/{tid}", json={"description": "Desc Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Part Updated"
    assert data["description"] == "Desc Updated"

@pytest.mark.anyio
async def test_update_ticket_not_found(client: AsyncClient):
    response = await client.put("/api/tickets/9999", json={"title": "Ghost"})
    assert response.status_code == 404

@pytest.mark.anyio
async def test_delete_ticket(client: AsyncClient):
    create = await client.post("/api/tickets/", json={"title": "Delete Me"})
    tid = create.json()["id"]
    
    response = await client.delete(f"/api/tickets/{tid}")
    assert response.status_code == 204
    
    # Verify gone
    get_res = await client.get(f"/api/tickets/{tid}")
    assert get_res.status_code == 404

@pytest.mark.anyio
async def test_delete_ticket_not_found(client: AsyncClient):
    response = await client.delete("/api/tickets/9999")
    assert response.status_code == 404

@pytest.mark.anyio
async def test_batch_delete_tickets(client: AsyncClient):
    t1 = await client.post("/api/tickets/", json={"title": "T1"})
    t2 = await client.post("/api/tickets/", json={"title": "T2"})
    ids = [t1.json()["id"], t2.json()["id"]]
    
    # FastAPI expects a list directly in the body for List[int]
    response = await client.request("DELETE", "/api/tickets/batch", json=ids)
    assert response.status_code == 204
    
    # Verify
    get_res = await client.get("/api/tickets/")
    current_ids = [t["id"] for t in get_res.json()["items"]]
    assert not any(i in current_ids for i in ids)

@pytest.mark.anyio
async def test_read_tickets_filter_search(client: AsyncClient):
    await client.post("/api/tickets/", json={"title": "Find Me"})
    await client.post("/api/tickets/", json={"title": "Ignore Me"})
    
    response = await client.get("/api/tickets/?q=Find")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Find Me"

@pytest.mark.anyio
async def test_read_tickets_filter_tag(client: AsyncClient):
    # Create tag
    tag = await client.post("/api/tags/", json={"name": "FilterTag"})
    tag_id = tag.json()["id"]
    
    # Create tickets
    await client.post("/api/tickets/", json={"title": "Tagged", "tags": [tag_id]})
    await client.post("/api/tickets/", json={"title": "Untagged"})
    
    response = await client.get(f"/api/tickets/?tag_id={tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Tagged"

@pytest.mark.anyio
async def test_read_tickets_pagination(client: AsyncClient):
    # Create 15 tickets
    for i in range(15):
        await client.post("/api/tickets/", json={"title": f"Ticket {i}"})
        
    response = await client.get("/api/tickets/?page=1&size=10")
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] >= 15
    
    response = await client.get("/api/tickets/?page=2&size=10")
    data = response.json()
    assert len(data["items"]) >= 5
