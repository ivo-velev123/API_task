from flask import Flask, jsonify, request, Response
import os
from backend.extensions import db
from dotenv import load_dotenv
from backend.models import Coin, Duty, Ksb
import json

app = Flask(__name__)

if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")

db.init_app(app)

load_dotenv()


@app.get("/coins")
def get_coins():
    coins = Coin.query.all()
    data = [coin.to_dict(include_duties=True) for coin in coins]
    return Response(json.dumps(data, sort_keys=False), mimetype="application/json")


@app.get("/coins/<ID>")
def get_coin_by_id(ID):
    coin = Coin.query.filter_by(id=ID).first()
    if not coin:
        return jsonify({"error": "Coin not found"}), 404
    return Response(
        json.dumps(coin.to_dict(include_duties=True), sort_keys=False),
        mimetype="application/json",
    )


@app.post("/coins")
def create_coin():
    data = request.json
    coin_name = data["coin_name"]
    duty_ids = data.get("duty_ids", [])

    new_coin = Coin(coin_name=coin_name)

    if duty_ids:
        duties = Duty.query.filter(Duty.id.in_(duty_ids)).all()
        new_coin.duties = duties

    db.session.add(new_coin)
    db.session.commit()
    return jsonify(new_coin.to_dict()), 201


@app.put("/coins/<ID>")
def update_coin(ID):
    data = request.json
    coin = Coin.query.filter_by(id=ID).first()

    if "coin_name" in data:
        coin.coin_name = data["coin_name"]

    if "duty_ids" in data:
        duty_ids = data["duty_ids"]

        new_duties = Duty.query.filter(Duty.id.in_(duty_ids)).all()
        coin.duties = new_duties

    db.session.commit()
    return Response(
        json.dumps(coin.to_dict(include_duties=True), sort_keys=False),
        mimetype="application/json",
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
    duties = Duty.query.all()
    data = [duty.to_dict(include_ksbs=True) for duty in duties]
    return Response(json.dumps(data, sort_keys=False), mimetype="application/json")


@app.get("/duties/<ID>")
def get_duties_by_id(ID):
    duty = Duty.query.filter_by(id=ID).first()
    if not duty:
        return jsonify({"error": "Duty not found"}), 404
    return Response(
        json.dumps(duty.to_dict(include_ksbs=True), sort_keys=False),
        mimetype="application/json",
    )


@app.post("/duties")
def create_duty():
    data = request.json
    duty_name = data["duty_name"]
    description = data.get("description", None)
    ksb_ids = data.get("ksb_ids", [])
    new_duty = Duty(duty_name=duty_name, duty_description=description)

    if ksb_ids:
        ksbs = Ksb.query.filter(Ksb.id.in_(ksb_ids)).all()
        new_duty.ksbs = ksbs

    db.session.add(new_duty)
    db.session.commit()
    return jsonify(new_duty.to_dict()), 201


@app.put("/duties/<ID>")
def update_duty(ID):
    data = request.json
    duty = Duty.query.filter_by(id=ID).first()

    if "duty_name" in data:
        duty.duty_name = data["duty_name"]

    if "ksb_ids" in data:
        ksb_ids = data["ksb_ids"]
        new_ksbs = Ksb.query.filter(Ksb.id.in_(ksb_ids)).all()
        duty.ksbs = new_ksbs

    db.session.commit()
    return Response(
        json.dumps(duty.to_dict(include_ksbs=True), sort_keys=False),
        mimetype="application/json",
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


@app.get("/ksbs/<ID>")
def get_ksb_by_id(ID):
    ksb = Ksb.query.filter_by(id=ID).first()
    if not ksb:
        return jsonify({"error": "Ksb not found"}), 404
    return Response(
        json.dumps(ksb.to_dict(), sort_keys=False), mimetype="application/json"
    )


@app.post("/ksbs")
def create_ksb():
    data = request.json
    ksb_name = data["ksb_name"]
    new_ksb = Ksb(ksb_name=ksb_name)
    db.session.add(new_ksb)
    db.session.commit()
    return jsonify(new_ksb.to_dict()), 201


@app.put("/ksbs/<ID>")
def update_ksb(ID):
    new_name = request.json["ksb_name"]
    ksb = Ksb.query.filter_by(id=ID).first()
    ksb.ksb_name = new_name
    db.session.commit()
    return Response(
        json.dumps(ksb.to_dict(), sort_keys=False), mimetype="application/json"
    )


@app.delete("/ksbs/<ID>")
def delete_ksb(ID):
    ksb = Ksb.query.filter_by(id=ID).first()
    if not ksb:
        return jsonify({"error": "Ksb not found"}), 404
    db.session.delete(ksb)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
