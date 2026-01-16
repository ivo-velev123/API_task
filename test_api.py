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
