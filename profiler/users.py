from flask import Blueprint

blueprint = Blueprint("users", __name__, url_prefix="/users")

@blueprint.route("/", methods=["POST"])
def create_user():
    return {"action": "create user"}, 201

@blueprint.route("/", methods=["GET"])
def list_users():
    return {"action": "list all users"}


@blueprint.route("/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    return {"action": f"get user {user_id}"}


@blueprint.route("/<int:user_id>/", methods=["PUT"])
def update_user(user_id):
    return {"action": f"update user {user_id}"}


@blueprint.route("/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    return "", 204