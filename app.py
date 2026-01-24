from flask import Flask, jsonify, request, Response
import os
from extensions import db
from dotenv import load_dotenv
from models import Coin, Duty, Ksb
import json

app = Flask(__name__)

if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")

db.init_app(app)

load_dotenv()


@app.get("/coins")
def get_coins():
    coins = Coin.query.all()
    data = [coin.to_dict() for coin in coins]
    return Response(json.dumps(data, sort_keys=False), mimetype="application/json")


@app.get("/coins/<ID>")
def get_coin_by_id(ID):
    coin = Coin.query.filter_by(id=ID).first()
    if not coin:
        return jsonify({"error": "Coin not found"}), 404
    return Response(
        json.dumps(coin.to_dict(), sort_keys=False), mimetype="application/json"
    )


@app.post("/coins")
def create_coin():
    data = request.json
    coin_name = data["coin_name"]
    new_coin = Coin(coin_name=coin_name)
    db.session.add(new_coin)
    db.session.commit()
    return jsonify(new_coin.to_dict()), 201


@app.put("/coins/<ID>")
def update_coin(ID):
    new_name = request.json["coin_name"]
    coin = Coin.query.filter_by(id=ID).first()
    coin.coin_name = new_name
    db.session.commit()
    return Response(
        json.dumps(coin.to_dict(), sort_keys=False), mimetype="application/json"
    )


@app.delete("/coins/<ID>")
def delete_coin(ID):
    coin = Coin.query.filter_by(id=ID).first()
    if not coin:
        return jsonify({"error": "Coin not found"}), 404
    db.session.delete(coin)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


@app.get("/duties")
def get_duties():
    duties = Duty().query.all()
    data = [duty.to_dict() for duty in duties]
    return Response(json.dumps(data, sort_keys=False), mimetype="application/json")


@app.get("/duties/<ID>")
def get_duties_by_id(ID):
    duty = Duty().query.filter_by(id=ID).first()
    if not duty:
        return jsonify({"error": "Duty not found"}), 404
    return Response(
        json.dumps(duty.to_dict(), sort_keys=False), mimetype="application/json"
    )


@app.post("/duties")
def create_duty():
    data = request.json
    duty_name = data["duty_name"]
    new_duty = Duty(duty_name=duty_name)
    db.session.add(new_duty)
    db.session.commit()
    return jsonify(new_duty.to_dict()), 201


@app.put("/duties/<ID>")
def update_duty(ID):
    new_name = request.json["duty_name"]
    duty = Duty.query.filter_by(id=ID).first()
    duty.duty_name = new_name
    db.session.commit()
    return Response(
        json.dumps(duty.to_dict(), sort_keys=False), mimetype="application/json"
    )


@app.delete("/duties/<ID>")
def delete_duty(ID):
    duty = Duty.query.filter_by(id=ID).first()
    if not duty:
        return jsonify({"error": "Duty not found"}), 404
    db.session.delete(duty)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


@app.get("/ksbs")
def get_ksbs():
    ksbs = Ksb.query.all()
    data = [ksb.to_dict() for ksb in ksbs]
    return Response(json.dumps(data, sort_keys=False), mimetype="application/json")


@app.post("/ksbs")
def create_ksb():
    data = request.json
    ksb_name = data["ksb_name"]
    new_ksb = Ksb(ksb_name=ksb_name)
    db.session.add(new_ksb)
    db.session.commit()
    return jsonify(new_ksb.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)
