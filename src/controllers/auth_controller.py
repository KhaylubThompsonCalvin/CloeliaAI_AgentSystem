# Auth Controller (Auth feature)
# Routes: /login, /register, /logout
# Uses flask-login and passlib for password hashing.
# src/controllers/auth_controller.py

from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required
from passlib.hash import bcrypt
from models.user_profile import UserProfile
from src.database import db  # SQLAlchemy object

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = bcrypt.hash(data.get("password"))

    user = UserProfile(username=username, password_hash=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"})

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = UserProfile.query.filter_by(username=data.get("username")).first()
    if user and bcrypt.verify(data.get("password"), user.password_hash):
        login_user(user)
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})
