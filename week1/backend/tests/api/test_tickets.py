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
async def test_read_tickets_filter(client: AsyncClient):
    await client.post("/api/tickets/", json={"title": "Find Me"})
    await client.post("/api/tickets/", json={"title": "Ignore Me"})
    
    response = await client.get("/api/tickets/?q=Find")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Find Me"
