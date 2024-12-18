"""
Этот модуль определяет маршруты API, связанные с логикой работы телеграм бота:
проверка связан ли аккаунт в телеграме с профилем на сайте, связвание и отвязка профиля от рассылки
"""

import os

from flasgger import swag_from
from flask import Blueprint, request, abort, jsonify

from webapp import db
from webapp.models.TelegramAccount import TelegramAccount
from webapp.models.User import User

notifications_bp = Blueprint("notifications_api", __name__)


SECRET_API_KEY = os.getenv("SECRET_API_KEY")


@notifications_bp.before_request
def check_secret_key():
    """
        Проверяет корректность переданного api ключа
        ---
        """

    values = request.values
    if "secret_key" not in values or values["secret_key"] != SECRET_API_KEY:
        abort(403)


@notifications_bp.errorhandler(403)
def handle_forbidden(e):
    """
        Отлавливает ошибку 403 - передан неверный api ключ
        ---
        """

    return {
        "success": False,
        "message": "Неверный api ключ"
    }, 403


@notifications_bp.route("/telegram-account/<int:acc_id>", methods=['GET'])
@swag_from("swagger_definitions/get_account_status.yaml")
def get_account_status(acc_id: int):
    """
        Проверяет статус подключения аккаунта
        ---
        """

    account = TelegramAccount.query.filter_by(telegram_user_id=acc_id).first()
    if account is None:
        return jsonify({
            "success": True,
            "connected": False,
            "user_id": None
        }), 200
    return jsonify({
        "success": True,
        "connected": True,
        "user_id": account.user.user_id
    }), 200


@notifications_bp.route("/telegram-account/<int:acc_id>", methods=['POST'])
@swag_from("swagger_definitions/connect_account.yaml")
def connect_account(acc_id: int):
    """
        Привязывает телеграм аккаунт к рассылке уведомлений
        ---
        """

    account_id = acc_id
    json_data = request.get_json()
    user = User.query.filter_by(email=json_data.get("user_email")).first()
    verification_code = json_data.get("verification_code")

    if user is None:
        return jsonify({
            "success": False,
            "message": "Пользователь не найден"
        }), 401

    if not user.is_verification_code_valid(verification_code):
        return jsonify({
            "success": False,
            "message": "Неверный код верификации"
        }), 400

    if not user.telegram_account is None:
        return jsonify({
            "success": False,
            "message": "У пользователя уже есть привязанный аккаунт"
        }), 400

    tg_acc_exists = TelegramAccount.query.filter_by(telegram_user_id=account_id).first()

    if not tg_acc_exists is None:
        return jsonify({
            "success": False,
             "message": "Данный телеграм аккаунт уже привязан"
        }), 400

    tg_acc = TelegramAccount(telegram_user_id=account_id, user_id=user.user_id)

    db.session.add(tg_acc)
    db.session.commit()

    return jsonify({
        "success": True
    }), 201


@notifications_bp.route("/telegram-account/<int:acc_id>", methods=['DELETE'])
@swag_from("swagger_definitions/delete_account.yaml")
def delete_account(acc_id: int):
    """
        Отвязывает телеграм аккаунт от рассылки уведомлений
        ---
        """

    account = TelegramAccount.query.filter_by(telegram_user_id=acc_id).first()
    if account is None:
        return jsonify({
            "success": False,
            "message": "Такого аккаунта не существует"
        }), 401

    db.session.delete(account)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Аккаунт успешно отключён от отправки уведомлений"
    }), 200