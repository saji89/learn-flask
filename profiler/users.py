from sqlite3.dbapi2 import Cursor
from flask import Blueprint, g, jsonify, request
from werkzeug.security import generate_password_hash

from .auth import login_required
from .db import get_db

blueprint = Blueprint("users", __name__, url_prefix="/users")

@blueprint.route("/", methods=["POST"])
def create_user():
    data = request.json

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, email, password]):
        return {"error": "Required fields are missing"}, 400

    db = get_db()

    hashed_password = generate_password_hash(password)

    try:
        cursor = db.execute(
            "INSERT INTO user (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, hashed_password),
        )
        db.commit()
    except db.IntegrityError:
        return {"error": "This email is already registered"}, 400

    return jsonify({"id": cursor.lastrowid}), 201

@blueprint.route("/", methods=["GET"])
@login_required
def list_users():
    db = get_db()

    cursor = db.execute("SELECT * FROM user")
    users = cursor.fetchall()

    user_list=[]
    for user in users:
        user_list.append(
            {
                "id": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": user["email"],
                "created_on": user["created_on"],                
            }
        )
    return jsonify(user_list)


@blueprint.route("/<int:user_id>/", methods=["GET"])
@login_required
def get_user(user_id):
    db = get_db()

    cursor = db.execute("SELECT * FROM user WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        return {"error": "Invalid user id"}, 404

    return {
        "id": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "created_on": user["created_on"],
    }


@blueprint.route("/<int:user_id>/", methods=["PUT"])
@login_required
def update_user(user_id):
    if user_id != g.user["id"]:
        return {"error": "Permission denied"}, 401

    data = request.json

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not all([first_name, last_name, email]):
        return {"error": "Required fields are missing"}, 400

    db = get_db()

    try:
        db.execute(
            "UPDATE user SET first_name=?, last_name=?, email=? WHERE id=?",
            (first_name, last_name, email, user_id),
        )
        db.commit()
    except db.IntegrityError:
        return {"error": "This email is already registered"}, 400

    return jsonify({"id": user_id}), 200


@blueprint.route("/<int:user_id>/", methods=["DELETE"])
@login_required
def delete_user(user_id):
    if user_id != g.user["id"]:
        return {"error": "Permission denied"}, 401

    db = get_db()

    db.execute("DELETE FROM user WHERE id=?", (user_id,))
    db.commit()

    return "", 204