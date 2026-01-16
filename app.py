from flask import Flask, jsonify, request
import os
from extensions import db
from dotenv import load_dotenv
from models import Coin


app = Flask(__name__)

if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")

db.init_app(app)

load_dotenv()


@app.get("/coins")
def get_coins():
    return jsonify([])


@app.post("/coins")
def create_coin():
    data = request.json
    coin_name = data["coin_name"]
    new_coin = Coin(coin_name=coin_name)
    db.session.add(new_coin)
    db.session.commit()
    return jsonify(new_coin.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)
