from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=True)

    @app.route("/")
    def hello():
        return {"message": "Hello, World!", "secret_key": app.config["SECRET_KEY"]}

    return app