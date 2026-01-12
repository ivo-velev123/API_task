from flask import Flask, jsonify
import os
from extensions import db
from dotenv import load_dotenv


app = Flask(__name__)

if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")

db.init_app(app)

load_dotenv

@app.route("/test")
def test():
    return jsonify("hello")


if __name__ == "__main__":
    app.run(debug=True)
