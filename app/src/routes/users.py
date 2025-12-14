from flask import Blueprint, request, jsonify
from src.models import User
from src.db import db

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    user = User(
        email=data["email"],
        name=data["name"]
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201
