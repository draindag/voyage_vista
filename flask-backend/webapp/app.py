"""
Модуль приложения Flask для Voyage Vista.

Этот модуль отвечает за создание и настройку приложения,
инициализацию необходимых компонентов и регистрацию маршрутов.
"""

import os
import sys
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError
from flask_uploads import IMAGES, configure_uploads

from jwt import ExpiredSignatureError, InvalidTokenError

from webapp import db, migrate, ma, swagger, jwt, photos
from webapp.routes import main_bp
from webapp.routes.accounting import accounting_bp
from webapp.routes.admin_panel import admin_bp
from webapp.routes.tours import tours_bp

load_dotenv()


def create_app(config: dict = None):
    """
    Создает экземпляр Flask-приложения с заданной конфигурацией.
        """

    app = Flask("voyage_vista")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        AUTH_SALT=os.getenv("AUTH_SALT"),
        SECRET_KEY=os.getenv("SECRET_KEY"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES"))),
        UPLOADED_PHOTOS_DEST=os.getenv("UPLOADED_PHOTOS_DEST"),
        UPLOADED_PHOTOS_URL=os.getenv("UPLOADED_PHOTOS_URL"),
        UPLOADED_PHOTOS_ALLOW= IMAGES,
        TOURS_PER_PAGE=os.getenv("TOURS_PER_PAGE"),
    )
    app.json.ensure_ascii = False

    if (os.getenv("AUTH_SALT") is None or os.getenv("FLASK_RUN_PORT") is None
            or os.getenv("SECRET_KEY") is None or os.getenv("JWT_SECRET_KEY") is None):
        sys.exit("!!!\nProgram needs a specified web_port/salt/secret/jwt_secret in settings\n!!!")

    if config is not None:
        app.config.update(config)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    ma.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    configure_uploads(app, photos)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
            'message': 'Страница не найдена'}), 404

    @app.errorhandler(NoAuthorizationError)
    def handle_missing_authorization_header(ex):
        return jsonify({"success": False,
            "message": "Отсутствует заголовок авторизации"}), 401

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token(ex):
        return jsonify({"success": False,
            "message": "Срок действия токена истек"}), 401

    @app.errorhandler(JWTDecodeError)
    def handle_jwt_decode_error(ex):
        return jsonify({"success": False,
            "message": "Не удалось декодировать токен"}), 401

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(ex):
        return jsonify({"success": False,
            "message": "Неверный токен"}), 401

    app.register_blueprint(main_bp)

    app.register_blueprint(tours_bp,  url_prefix="/api/tours")

    app.register_blueprint(accounting_bp, url_prefix="/api")

    app.register_blueprint(admin_bp, url_prefix="/api/admin_panel")

    return app
