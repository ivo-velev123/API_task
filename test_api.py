import pytest
import os

os.environ["db_url"] = "sqlite:///:memory:"

from app import app, db
from models import Coin, Duty, Ksb


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()

            yield test_client

            db.drop_all()


class TestCoins:
    def test_get_coins_empty(self, client):
        response = client.get("/coins")
        assert response.status_code == 200
        assert response.json == []

    def test_create_coin(self, client):
        test_coin_data = {"coin_name": "automate"}
        response = client.post("/coins", json=test_coin_data)
        assert response.status_code == 201
        assert response.json["coin_name"] == "automate"
        assert response.json["id"] is not None

    def test_get_all_coins(self, client):
        test_coin_data = {"coin_name": "automate"}
        client.post("/coins", json=test_coin_data)
        response = client.get("/coins")
        assert response.status_code == 200
        assert len(response.json) > 0
        assert response.json[0]["coin_name"] == "automate"

    def test_get_coin_by_id(self, client):
        test_coin_data = {"coin_name": "automate"}
        post_response = client.post("/coins", json=test_coin_data)
        coin_id = post_response.json["id"]
        response = client.get(f"/coins/{coin_id}")
        assert response.status_code == 200
        assert response.json["id"] == coin_id
        assert response.json["coin_name"] == "automate"

    def test_update_coin(self, client):
        test_coin_data = {"coin_name": "automate"}
        post_response = client.post("/coins", json=test_coin_data)
        coin_id = post_response.json["id"]
        test_update_data = {"coin_name": "houston"}
        response = client.put(f"/coins/{coin_id}", json=test_update_data)
        assert response.status_code == 200
        assert response.json["coin_name"] == "houston"
        get_response = client.get(f"/coins/{coin_id}")
        assert get_response.json["coin_name"] == "houston"

    def test_delete_coin(self, client):
        test_coin_data = {"coin_name": "automate"}
        post_response = client.post("/coins", json=test_coin_data)
        coin_id = post_response.json["id"]
        delete_response = client.delete(f"/coins/{coin_id}")
        assert delete_response.status_code == 200
        assert delete_response.json["message"] == "deleted"
        get_response = client.get(f"/coins/{coin_id}")
        assert get_response.status_code == 404
        assert get_response.json["error"] == "Coin not found"


class TestDuty:
    def test_get_duty_empty(self, client):
        response = client.get("/duties")
        assert response.status_code == 200
        assert response.json == []

    def test_create_duty(self, client):
        test_duty_data = {"duty_name": "duty_1"}
        response = client.post("/duties", json=test_duty_data)
        assert response.status_code == 201
        assert response.json["duty_name"] == "duty_1"
        assert response.json["id"] is not None

    def get_all_duties(self, client):
        test_duty_data = {"duty_name": "duty_1"}
        client.post("/coins", json=test_duty_data)
        response = client.get("/coins")
        assert response.status_code == 200
        assert len(response.json) > 0
        assert response.json[0]["duty_name"] == "duty_1"

    def test_get_duty_by_id(self, client):
        test_duty_data = {"duty_name": "duty_1"}
        post_response = client.post("/duties", json=test_duty_data)
        duty_id = post_response.json["id"]
        response = client.get(f"/duties/{duty_id}")
        assert response.status_code == 200
        assert response.json["id"] == duty_id
        assert response.json["duty_name"] == "duty_1"
