from flask import Blueprint

blueprint = Blueprint("users", __name__, url_prefix="/users")

@blueprint.route("/", method=["POST"])
def create_user():
    return("message": "Creating enw user")