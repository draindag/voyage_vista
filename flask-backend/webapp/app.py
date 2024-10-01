import os
import sys

from dotenv import load_dotenv
from flask import Flask
from webapp import db, migrate
from webapp.routes import main_bp


load_dotenv()


def create_app(config: dict = None):
    app = Flask("voyage_vista")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        AUTH_SALT=os.getenv("AUTH_SALT"),
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )

    if os.getenv("AUTH_SALT") is None or os.getenv("FLASK_RUN_PORT") is None or os.getenv("SECRET_KEY") is None:
        sys.exit("!!!!!!\nProgram needs a specified web_port/salt/secret in settings\n!!!!!!")

    if config is not None:
        app.config.update(config)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)

    return app
