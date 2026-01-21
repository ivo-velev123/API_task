from flask import Flask, jsonify, request, Response
import os
from extensions import db
from dotenv import load_dotenv
from models import Coin
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
        return Response(json.dumps({"error": "Coin not found"}), 404)
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
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
