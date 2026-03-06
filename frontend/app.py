from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")


@app.route('/')
def index():
    all_coins = requests.get(f"{BACKEND_URL}/coins").json()

    selected_duty = None
    linked_coins = []

    duty_id = request.args.get("duty_id")
    if duty_id:
        selected_duty = requests.get(f"{BACKEND_URL}/duties/{duty_id}").json()
        linked_coins = [
            coin for coin in all_coins
            if any(d["id"] == duty_id for d in coin.get("duties", []))
        ]

    return render_template("index.html", coins=all_coins, selected_duty=selected_duty, linked_coins=linked_coins)
