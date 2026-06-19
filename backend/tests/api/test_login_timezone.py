import pytest


@pytest.mark.asyncio
async def test_login_updates_timezone(client):
    await client.post(
        "/auth/register",
        json={"email": "tz@example.com", "password": "password123", "timezone": "UTC"},
    )
    response = await client.post(
        "/auth/login",
        json={
            "email": "tz@example.com",
            "password": "password123",
            "timezone": "Europe/Moscow",
        },
    )
    assert response.status_code == 200
    assert response.json()["timezone"] == "Europe/Moscow"

    me = await client.get("/auth/me")
    assert me.status_code == 200
    assert me.json()["timezone"] == "Europe/Moscow"
