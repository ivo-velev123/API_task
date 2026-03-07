import sys
sys.path.insert(0, "/app")

from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    users = [
        ("admin", generate_password_hash("adminpass"), "admin"),
        ("user", generate_password_hash("userpass"), "user"),
    ]
    for username, password, role in users:
        if not User.query.filter_by(username=username).first():
            db.session.add(User(username=username, password=password, role=role))
    db.session.commit()
    print("users created")