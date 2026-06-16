import pytest
from uuid import UUID


@pytest.mark.asyncio
async def test_register_sets_cookie(auth_client):
    client, user_id = auth_client
    assert isinstance(user_id, UUID)


@pytest.mark.asyncio
async def test_create_entry(auth_client):
    client, _ = auth_client
    response = await client.post(
        "/entries",
        json={"raw_text": "починил баг с API"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["entry"]["raw_text"] == "починил баг с API"
    assert data["suggestion"]["confidence"] > 0


@pytest.mark.asyncio
async def test_list_entries(auth_client):
    client, _ = auth_client
    await client.post("/entries", json={"raw_text": "сделал макет"})
    response = await client.get("/entries")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_weekly_report(auth_client):
    client, _ = auth_client
    await client.post("/entries", json={"raw_text": "читал про postgres"})
    response = await client.get("/reports/weekly")
    assert response.status_code == 200
    assert response.json()["total_entries"] >= 1


@pytest.mark.asyncio
async def test_today_report(auth_client):
    client, _ = auth_client
    await client.post("/entries", json={"raw_text": "позвонил клиенту"})
    response = await client.get("/reports/today")
    assert response.status_code == 200
    assert response.json()["entry_count"] >= 1


@pytest.mark.asyncio
async def test_unauthenticated_entries(client):
    response = await client.post("/entries", json={"raw_text": "test"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_entry_mood_and_category(auth_client):
    client, _ = auth_client
    create = await client.post(
        "/entries",
        json={"raw_text": "читал про postgres", "mood": 3},
    )
    entry_id = create.json()["entry"]["id"]

    patch = await client.patch(
        f"/entries/{entry_id}",
        json={"mood": 5, "category": "learning"},
    )
    assert patch.status_code == 200, patch.text
    data = patch.json()
    assert data["mood"] == 5
    assert data["tags"][0]["category"] == "learning"
    assert data["raw_text"] == "читал про postgres"


@pytest.mark.asyncio
async def test_delete_entry(auth_client):
    client, _ = auth_client
    create = await client.post("/entries", json={"raw_text": "удалить меня"})
    entry_id = create.json()["entry"]["id"]

    delete = await client.delete(f"/entries/{entry_id}")
    assert delete.status_code == 204

    listing = await client.get("/entries")
    assert all(item["id"] != entry_id for item in listing.json())


@pytest.mark.asyncio
async def test_cross_user_patch_not_found(app, use_cases):
    from httpx import ASGITransport, AsyncClient
    from reverse_todo.config import get_settings
    from reverse_todo.infrastructure.di import get_session, get_use_cases
    from reverse_todo.api.deps import get_current_user, get_current_user_id

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post(
            "/auth/register",
            json={"email": "u1@test.com", "password": "password123"},
        )
        create_resp = await c.post("/entries", json={"raw_text": "work item"})
        entry_id = create_resp.json()["entry"]["id"]

        await c.post("/auth/logout")
        await c.post(
            "/auth/register",
            json={"email": "u2@test.com", "password": "password123"},
        )
        patch = await c.patch(f"/entries/{entry_id}", json={"tag_ids": []})
        assert patch.status_code == 404

    get_settings.cache_clear()
