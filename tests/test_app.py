"""
Общие тесты приложения
"""

from flask import Flask
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError, InvalidTokenError



def test_app_creation(app):
    """
    Проверяем, что приложение Flask создается без ошибок и имеет правильные настройки.
    """
    assert isinstance(app, Flask)
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_app_blueprints(app):
    """
    Проверяем, что все зарегистрированные blueprints присутствуют в приложении.
    """
    blueprints = app.blueprints.keys()

    assert "main" in blueprints
    assert "tours" in blueprints
    assert "accounting" in blueprints
    assert "admin_panel" in blueprints


def test_404_error_handling(client):
    """
    Проверяем обработку ошибки 404.
    """
    response = client.get("/non-existent-route")
    assert response.status_code == 404

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страница не найдена"


def test_handle_missing_authorization_header(app):
    """
    Проверяем обработку ошибки NoAuthorizationError.
    """
    @app.route("/protected")
    def protected_route():
        raise NoAuthorizationError()

    client = app.test_client()
    response = client.get("/protected")

    assert response.status_code == 401

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Отсутствует заголовок авторизации"


def test_handle_expired_token(app):
    """
    Проверяем обработку ошибки ExpiredSignatureError.
    """
    @app.route("/expired")
    def expired_route():
        raise ExpiredSignatureError()

    client = app.test_client()
    response = client.get("/expired")

    assert response.status_code == 401

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Срок действия токена истек"


def test_handle_invalid_token(app):
    """
    Проверяем обработку ошибки InvalidTokenError.
    """
    @app.route("/invalid-token")
    def invalid_token_route():
        raise InvalidTokenError()

    client = app.test_client()
    response = client.get("/invalid-token")

    assert response.status_code == 401

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неверный токен"