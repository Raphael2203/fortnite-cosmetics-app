from tests.test_purchases import setup_test_data, client

def test_get_users_public():
    td = setup_test_data()
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(u["id"] == td["user_id"] for u in data)

def test_get_user_profile_with_acquired_cosmetics():
    td = setup_test_data()
    user_id = td["user_id"]
    cosmetic_id = td["cosmetic_ids"][0]
    # buy one cosmetic so it appears on profile
    buy_resp = client.post(f"/purchases/buy/cosmetic/{cosmetic_id}")
    assert buy_resp.status_code == 200

    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert "acquired_cosmetics" in data
    assert any(c["id"] == cosmetic_id for c in data["acquired_cosmetics"])
