from flask import Flask, jsonify
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
    return ("", 201)


if __name__ == "__main__":
    app.run(debug=True)
