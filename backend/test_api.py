import pytest
import os

os.environ["db_url"] = "sqlite:///:memory:"

from backend.app import app, db
from backend.models import Coin, Duty


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


class TestDutys:
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

    def test_update_duty(self, client):
        test_duty_data = {"duty_name": "duty_1"}
        post_response = client.post("/duties", json=test_duty_data)
        duty_id = post_response.json["id"]
        test_update_data = {"duty_name": "duty_2"}
        response = client.put(f"/duties/{duty_id}", json=test_update_data)
        assert response.status_code == 200
        assert response.json["duty_name"] == "duty_2"
        get_response = client.get(f"/duties/{duty_id}")
        assert get_response.status_code == 200
        assert get_response.json["duty_name"] == "duty_2"

    def test_delete_duty(self, client):
        test_duty_data = {"duty_name": "duty_1"}
        post_response = client.post("/duties", json=test_duty_data)
        duty_id = post_response.json["id"]
        delete_response = client.delete(f"/duties/{duty_id}")
        assert delete_response.status_code == 200
        assert delete_response.json["message"] == "deleted"
        get_response = client.get(f"/duties/{duty_id}")
        assert get_response.status_code == 404
        assert get_response.json["error"] == "Duty not found"

    def test_duty_has_description(self, client):
        test_duty_data = {"duty_name": "duty_1", "description": "this is a description"}
        response = client.post("/duties", json=test_duty_data)
        duty_id = response.json["id"]
        assert response.status_code == 201

        get_response = client.get(f"/duties/{duty_id}")
        assert get_response.status_code == 200
        assert get_response.json["description"] == "this is a description"

    def test_duty_description_is_optional(self, client):
        test_duty_data = {"duty_name": "duty_1"}
        response = client.post("/duties", json=test_duty_data)
        assert response.status_code == 201
        assert response.json["description"] is None

class TestKsbs:
    def test_get_empty_ksbs(self, client):
        response = client.get("/ksbs")
        assert response.status_code == 200
        assert response.json == []

    def test_create_ksb(self, client):
        test_ksb_data = {"ksb_name": "K1"}
        response = client.post("/ksbs", json=test_ksb_data)
        assert response.status_code == 201
        assert response.json["ksb_name"] == "K1"
        assert response.json["id"] is not None

    def test_get_all_ksbs(self, client):
        test_ksb_data = {"ksb_name": "K1"}
        post_response = client.post("/ksbs", json=test_ksb_data)
        ksb_id = post_response.json["id"]
        response = client.get("/ksbs")
        assert response.status_code == 200
        assert response.json[0]["ksb_name"] == "K1"
        assert response.json[0]["id"] == ksb_id

    def test_get_ksb_by_id(self, client):
        test_ksb_data = {"ksb_name": "K1"}
        post_response = client.post("/ksbs", json=test_ksb_data)
        ksb_id = post_response.json["id"]
        response = client.get(f"/ksbs/{ksb_id}")
        assert response.status_code == 200
        assert response.json["id"] == ksb_id
        assert response.json["ksb_name"] == "K1"

    def test_update_ksb(self, client):
        test_ksb_data = {"ksb_name": "K1"}
        post_response = client.post("/ksbs", json=test_ksb_data)
        ksb_id = post_response.json["id"]
        test_update_data = {"ksb_name": "K2"}
        put_response = client.put(f"/ksbs/{ksb_id}", json=test_update_data)
        assert put_response.status_code == 200
        assert put_response.json["ksb_name"] == "K2"
        get_response = client.get(f"/ksbs/{ksb_id}")
        assert get_response.status_code == 200
        assert get_response.json["ksb_name"] == "K2"
        assert get_response.json["id"] == ksb_id

    def test_delete_ksb(self, client):
        test_ksb_data = {"ksb_name": "K1"}
        post_response = client.post("/ksbs", json=test_ksb_data)
        ksb_id = post_response.json["id"]
        delete_response = client.delete(f"/ksbs/{ksb_id}")
        assert delete_response.status_code == 200
        assert delete_response.json["message"] == "deleted"
        get_response = client.get(f"/ksbs/{ksb_id}")
        assert get_response.status_code == 404
        assert get_response.json["error"] == "Ksb not found"


class TestCoinDutyRelationships:
    def test_create_coin_with_duties(self, client):
        duty1_test_data = {"duty_name": "duty_1"}
        duty1_response = client.post("/duties", json=duty1_test_data)
        duty1_id = duty1_response.json["id"]

        duty2_test_data = {"duty_name": "duty_2"}
        duty2_response = client.post("/duties", json=duty2_test_data)
        duty2_id = duty2_response.json["id"]

        coin_data = {"coin_name": "automate", "duty_ids": [duty1_id, duty2_id]}
        coin_response = client.post("/coins", json=coin_data)
        coin_id = coin_response.json["id"]

        assert coin_response.status_code == 201
        assert coin_response.json["coin_name"] == "automate"

        coin = Coin.query.get(coin_id)
        assert len(coin.duties) == 2

    def test_get_coin_with_duties(self, client):
        duty1_test_data = {"duty_name": "duty_1"}
        duty1_response = client.post("/duties", json=duty1_test_data)
        duty1_id = duty1_response.json["id"]

        duty2_test_data = {"duty_name": "duty_2"}
        duty2_response = client.post("/duties", json=duty2_test_data)
        duty2_id = duty2_response.json["id"]

        coin_data = {"coin_name": "automate", "duty_ids": [duty1_id, duty2_id]}
        coin_response = client.post("/coins", json=coin_data)
        coin_id = coin_response.json["id"]

        response = client.get(f"/coins/{coin_id}")

        assert response.status_code == 200
        assert "duties" in response.json
        assert len(response.json["duties"]) == 2
        assert response.json["duties"][0]["duty_name"] in ["duty_1", "duty_2"]
        assert response.json["duties"][1]["duty_name"] in ["duty_1", "duty_2"]

    def test_get_all_coins_with_duties(self, client):
        duty1_test_data = {"duty_name": "duty_1"}
        duty1_response = client.post("/duties", json=duty1_test_data)
        duty1_id = duty1_response.json["id"]

        duty2_test_data = {"duty_name": "duty_2"}
        duty2_response = client.post("/duties", json=duty2_test_data)
        duty2_id = duty2_response.json["id"]

        coin1_data = {"coin_name": "coin_1", "duty_ids": [duty1_id]}
        client.post("/coins", json=coin1_data)

        coin2_data = {"coin_name": "coin_2", "duty_ids": [duty2_id]}
        client.post("/coins", json=coin2_data)

        response = client.get("/coins")

        assert response.status_code == 200
        assert len(response.json) == 2

        assert "duties" in response.json[0]
        assert len(response.json[0]["duties"]) == 1

        assert "duties" in response.json[1]
        assert len(response.json[1]["duties"]) == 1

    def test_update_coin_duties(self, client):
        duty1_test_data = {"duty_name": "duty_1"}
        duty1_response = client.post("/duties", json=duty1_test_data)
        duty1_id = duty1_response.json["id"]

        duty2_test_data = {"duty_name": "duty_2"}
        duty2_response = client.post("/duties", json=duty2_test_data)
        duty2_id = duty2_response.json["id"]

        duty3_test_data = {"duty_name": "duty_3"}
        duty3_response = client.post("/duties", json=duty3_test_data)
        duty3_id = duty3_response.json["id"]

        coin_data = {"coin_name": "automate", "duty_ids": [duty1_id, duty2_id]}
        coin_response = client.post("/coins", json=coin_data)
        coin_id = coin_response.json["id"]

        update_data = {"coin_name": "automate", "duty_ids": [duty2_id, duty3_id]}
        response = client.put(f"/coins/{coin_id}", json=update_data)

        assert response.status_code == 200

        coin = Coin.query.get(coin_id)
        assert len(coin.duties) == 2
        duty_ids = [duty.id for duty in coin.duties]
        assert duty2_id in duty_ids
        assert duty3_id in duty_ids
        assert duty1_id not in duty_ids


class TestDutyKsbRelationships:
    def test_create_duty_with_ksbs(self, client):
        ksb1_test_data = {"ksb_name": "K1"}
        ksb1_response = client.post("/ksbs", json=ksb1_test_data)
        ksb1_id = ksb1_response.json["id"]

        ksb2_test_data = {"ksb_name": "K2"}
        ksb2_response = client.post("/ksbs", json=ksb2_test_data)
        ksb2_id = ksb2_response.json["id"]

        duty_data = {"duty_name": "duty_1", "ksb_ids": [ksb1_id, ksb2_id]}
        duty_response = client.post("/duties", json=duty_data)
        duty_id = duty_response.json["id"]

        assert duty_response.status_code == 201
        assert duty_response.json["duty_name"] == "duty_1"

        duty = Duty.query.get(duty_id)
        assert len(duty.ksbs) == 2

    def test_get_duty_with_ksbs(self, client):
        ksb1_test_data = {"ksb_name": "K1"}
        ksb1_response = client.post("/ksbs", json=ksb1_test_data)
        ksb1_id = ksb1_response.json["id"]

        ksb2_test_data = {"ksb_name": "K2"}
        ksb2_response = client.post("/ksbs", json=ksb2_test_data)
        ksb2_id = ksb2_response.json["id"]

        duty_data = {"duty_name": "duty_1", "ksb_ids": [ksb1_id, ksb2_id]}
        duty_response = client.post("/duties", json=duty_data)
        duty_id = duty_response.json["id"]

        response = client.get(f"/duties/{duty_id}")

        assert response.status_code == 200
        assert "ksbs" in response.json
        assert len(response.json["ksbs"]) == 2
        assert response.json["ksbs"][0]["ksb_name"] in ["K1", "K2"]
        assert response.json["ksbs"][1]["ksb_name"] in ["K1", "K2"]

    def test_get_all_duties_with_ksbs(self, client):
        ksb1_test_data = {"ksb_name": "K1"}
        ksb1_response = client.post("/ksbs", json=ksb1_test_data)
        ksb1_id = ksb1_response.json["id"]

        ksb2_test_data = {"ksb_name": "K2"}
        ksb2_response = client.post("/ksbs", json=ksb2_test_data)
        ksb2_id = ksb2_response.json["id"]

        duty1_data = {"duty_name": "duty_1", "ksb_ids": [ksb1_id]}
        client.post("/duties", json=duty1_data)

        duty2_data = {"duty_name": "duty_2", "ksb_ids": [ksb2_id]}
        client.post("/duties", json=duty2_data)

        response = client.get("/duties")

        assert response.status_code == 200
        assert len(response.json) == 2

        assert "ksbs" in response.json[0]
        assert len(response.json[0]["ksbs"]) == 1

        assert "ksbs" in response.json[1]
        assert len(response.json[1]["ksbs"]) == 1

    def test_update_duty_ksbs(self, client):
        ksb1_test_data = {"ksb_name": "K1"}
        ksb1_response = client.post("/ksbs", json=ksb1_test_data)
        ksb1_id = ksb1_response.json["id"]

        ksb2_test_data = {"ksb_name": "K2"}
        ksb2_response = client.post("/ksbs", json=ksb2_test_data)
        ksb2_id = ksb2_response.json["id"]

        ksb3_test_data = {"ksb_name": "K3"}
        ksb3_response = client.post("/ksbs", json=ksb3_test_data)
        ksb3_id = ksb3_response.json["id"]

        duty_data = {"duty_name": "duty_1", "ksb_ids": [ksb1_id, ksb2_id]}
        duty_response = client.post("/duties", json=duty_data)
        duty_id = duty_response.json["id"]

        update_data = {"duty_name": "duty_1", "ksb_ids": [ksb2_id, ksb3_id]}
        response = client.put(f"/duties/{duty_id}", json=update_data)

        assert response.status_code == 200

        duty = Duty.query.get(duty_id)
        assert len(duty.ksbs) == 2

        ksb_ids = [ksb.id for ksb in duty.ksbs]
        assert ksb2_id in ksb_ids
        assert ksb3_id in ksb_ids
        assert ksb1_id not in ksb_ids
