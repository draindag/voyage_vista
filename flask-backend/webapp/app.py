import os
import sys

from dotenv import load_dotenv
from flask import Flask, make_response, jsonify
from webapp import db, migrate, ma, swagger
from webapp.routes import main_bp
from webapp.routes.admin_panel import admin_bp
from webapp.routes.tours import tours_bp

load_dotenv()


def create_app(config: dict = None):
    app = Flask("voyage_vista")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        AUTH_SALT=os.getenv("AUTH_SALT"),
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )
    app.json.ensure_ascii = False

    if os.getenv("AUTH_SALT") is None or os.getenv("FLASK_RUN_PORT") is None or os.getenv("SECRET_KEY") is None:
        sys.exit("!!!!!!\nProgram needs a specified web_port/salt/secret in settings\n!!!!!!")

    if config is not None:
        app.config.update(config)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    ma.init_app(app)
    swagger.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    app.register_blueprint(main_bp)

    app.register_blueprint(tours_bp,  url_prefix="/api/tours")

    app.register_blueprint(admin_bp, url_prefix="/api/admin_panel")

    return app
