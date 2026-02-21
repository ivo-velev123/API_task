from flask import Flask, render_template, abort
import os
import requests

app=Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL")

@app.get("/")
def index():
    response = requests.get(f"{BACKEND_URL}/coins")
    if not response.ok:
        abort(response.status_code)
    coins = response.json()
    return render_template("index.html", coins=coins)

@app.get("/coins/<id>/duties")
def coin_duties(id):
    response = requests.get(f"{BACKEND_URL}/coins/{id}")
    if not response.ok:
        abort(response.status_code)
    coin = response.json()
    return render_template("partials/coin_duties.html", coin=coin)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)