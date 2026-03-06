from flask import Flask, render_template, request, session, redirect
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
completions = set()

@app.route('/')
def index():
    all_coins = requests.get(f"{BACKEND_URL}/coins").json()
    for coin in all_coins:
        coin["completed"] = coin["id"] in completions

    selected_duty = None
    linked_coins = []

    duty_id = request.args.get("duty_id")
    if duty_id:
        selected_duty = requests.get(f"{BACKEND_URL}/duties/{duty_id}").json()
        linked_coins = [
            coin for coin in all_coins
            if any(d["id"] == duty_id for d in coin.get("duties", []))
        ]

    return render_template("index.html", coins=all_coins, selected_duty=selected_duty, linked_coins=linked_coins, role=session.get("role", "anonymous"), session=session)

@app.get("/login")
def login_page():
    return render_template("login.html")
@app.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session["username"] = username
        session["role"] = user.role
        return redirect("/")
    return render_template("login.html", error="Invalid username or password")

@app.post("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.post("/coins/<id>/toggle")
def toggle_coin(id):
    if session.get("role") not in ("user", "admin"):
        return redirect("/login")
    if id in completions:
        completions.discard(id)
    else:
        completions.add(id)
    return redirect("/")

@app.get("/admin")
def admin_page():
    if session.get("role") != "admin":
        return redirect("/")
    coins = requests.get(f"{BACKEND_URL}/coins").json()
    duties = requests.get(f"{BACKEND_URL}/duties").json()
    return render_template("admin.html", coins=coins, duties=duties)

@app.post("/admin/coins")
def create_coin():
    if session.get("role") != "admin":
        return redirect("/")
    duty_ids = request.form.getlist("duty_ids")
    requests.post(f"{BACKEND_URL}/coins", json={"coin_name": request.form["coin_name"], "duty_ids": duty_ids})

    return redirect("/admin")

@app.post("/admin/coins/<id>/delete")
def delete_coin(id):
    if session.get("role") != "admin":
        return redirect("/")
    requests.delete(f"{BACKEND_URL}/coins/{id}")
    return redirect("/admin")
