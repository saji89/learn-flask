import jwt
from flask import Blueprint, current_app, request
from werkzeug.security import check_password_hash

from .db import get_db

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def generate_token(user_id):
    payload = {"id": user_id}
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(
            token, current_app.config["JWT_SECRET"], algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidSignatureError:
        return None

    return payload["id"]


@blueprint.route("/get-token/", methods=["POST"])
def get_token():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    db = get_db()
    cursor = db.execute("SELECT * FROM user where email=?", (email,))
    user = cursor.fetchone()

    if user is None:
        return {"error": "Incorrect email"}, 401

    if not check_password_hash(user["password"], password):
        return {"error": "Incorrect password"}, 401

    token = generate_token(user["id"])

    return {"user_id": user["id"], "token": token}