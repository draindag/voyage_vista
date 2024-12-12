"""
Этот модуль определяет маршруты API, связанные с пользователями веб-сайта:
регистрация, вход, личный кабинет и изменение личных данных
"""

from functools import wraps

from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from marshmallow import ValidationError, EXCLUDE

from webapp import db
from webapp.models.User import User
from webapp.schemas.EditLoginSchema import EditLoginSchema
from webapp.schemas.LoginSchema import LoginSchema
from webapp.schemas.RegistrationSchema import RegistrationSchema
from webapp.schemas.UserSchema import UserSchema

accounting_bp = Blueprint("accounting", __name__)


def anonymous_required(fn):
    """
        Функция обертка для api-путей, куда возможно попасть только без jwt токена
        ---
        """

    @wraps(fn)
    @jwt_required(optional=True)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity:
            return jsonify({"success": False,
                "message": "Пользователь уже авторизован"}), 403
        return fn(*args, **kwargs)
    return wrapper


@accounting_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@swag_from("swagger_definitions/refresh.yaml")
def refresh():
    """
        Обновляет access токен
        ---
        """

    user_login = get_jwt_identity()
    access_token = create_access_token(identity=user_login)
    return jsonify({"success": True,
        "access_token": access_token}), 200


@accounting_bp.route('/registration', methods=['POST'])
@anonymous_required
@swag_from("swagger_definitions/registration.yaml")
def registration():
    """
       Регистрация пользователя
       ---
       """

    json_data = request.get_json()

    email_registered = User.query.filter_by(email=json_data.get("email")).first()
    if email_registered:
        return {"success": False,
                "message": "Пользователь с таким логином или email уже зарегистрирован!"}, 400

    login_registered = User.query.filter_by(login=json_data.get("login")).first()
    if login_registered:
        return {"success": False,
                "message": "Пользователь с таким логином или email уже зарегистрирован!"}, 400


    registration_schema = RegistrationSchema(unknown=EXCLUDE)

    try:
        user_data = registration_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                        "errors": err.messages}), 400

    new_user = User(
        login=user_data['login'],
        email=user_data['email'],
    )
    new_user.set_password(user_data['password'])

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.login)
    refresh_token = create_refresh_token(identity=new_user.login)

    return jsonify({
        "success": True,
        "message": "Пользователь успешно зарегистрирован!",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": "visitor"
    }), 201


@accounting_bp.route('/login', methods=['POST'])
@anonymous_required
@swag_from("swagger_definitions/login.yaml")
def login():
    """
       Вход в аккаунт
       ---
       """

    json_data = request.get_json()

    login_schema = LoginSchema(unknown=EXCLUDE)

    try:
        user_data = login_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                        "errors": err.messages}), 400

    user = User.query.filter_by(email=user_data["email"]).first()

    if user and user.check_password(user_data["password"]):

        access_token  = create_access_token(identity=user.login)
        refresh_token = create_refresh_token(identity=user.login)
        return jsonify({"success": True,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "role": user.role
        }), 200

    return jsonify({"success": False,
        "message": "Неверная информация в полях авторизации"}), 400


@accounting_bp.route('/profile', methods=['GET'])
@jwt_required()
@swag_from("swagger_definitions/show_profile.yaml")
def show_profile():
    """
        Возвращает все данные пользователя для личного кабинета
        ---
        """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False,
                        "message": "Пользователь не найден"}), 401

    user_schema = UserSchema(unknown=EXCLUDE)
    return jsonify({"success": True,
                    "user": user_schema.dump(current_user)}), 200


@accounting_bp.route('/edit_email', methods=['PUT'])
@jwt_required()
@swag_from("swagger_definitions/edit_email.yaml")
def edit_email():
    """
       Изменение email пользователя
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False,
                "message": "Пользователь не найден"}), 401

    json_data = request.get_json()

    login_schema = LoginSchema(unknown=EXCLUDE)

    try:
        user_data = login_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                        "errors": err.messages}), 400

    new_email = json_data.get("email")

    email_registered = User.query.filter_by(email=new_email).first()
    if email_registered:
        return {"success": False,
                "message": "Невозможно использовать данный email!"}, 400

    if not current_user.check_password(json_data.get("password")):
        return jsonify({"success": False,
                        "message": "Неверный пароль!"}), 400

    current_user.set_email(new_email)
    db.session.commit()

    return jsonify({"success": True,
            "message": "Email успешно изменён!"}), 200


@accounting_bp.route('/edit_login', methods=['PUT'])
@jwt_required()
@swag_from("swagger_definitions/edit_login.yaml")
def edit_login():
    """
       Изменение логина пользователя
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False,
                        "message": "Пользователь не найден"}), 401

    json_data = request.get_json()

    edit_login_schema = EditLoginSchema(unknown=EXCLUDE)

    try:
        user_data = edit_login_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                        "errors": err.messages}), 400

    new_login = json_data.get("new_login")

    login_registered = User.query.filter_by(login=json_data.get("login")).first()

    if login_registered:
        return {"success": False,
                "message": "Невозможно использовать данный логин!"}, 400

    if not current_user.check_password(json_data.get("password")):
        return jsonify({"success": False,
                        "message": "Неверный пароль!"}), 400

    current_user.set_login(new_login)
    db.session.commit()

    access_token = create_access_token(identity=current_user.login)
    refresh_token = create_refresh_token(identity=current_user.login)
    return jsonify({"success": True,
                    "message": "Логин успешно изменён!",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                    }), 200


@accounting_bp.route('/edit_password', methods=['PUT'])
@jwt_required()
@swag_from("swagger_definitions/edit_password.yaml")
def edit_password():
    """
       Изменение пароля пользователя
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False,
                        "message": "Пользователь не найден"}), 401

    json_data = request.get_json()

    old_password = json_data.get("old_password")
    new_password = json_data.get("new_password")

    if not current_user.check_password(old_password):
        return {"success": False,
                "message": "Неверный старый пароль!"}, 400

    if not new_password.strip():
        return {"success": False,
                "message": "Пароль не может быть пустым!"}, 400

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({"success": True,
            "message": "Пароль успешно изменён!"}), 200
