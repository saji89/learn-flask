from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=True)

    from . import db
    db.init_app(app)

    return app
