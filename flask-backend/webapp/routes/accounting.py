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
@swag_from({
    'responses': {
        200: {
            'description': 'Обновил и вернул access токен'
        },
        401: {
            'description': 'refresh токен не прошел проверку'
        }
    },
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'description': 'JWT refresh токен для обновления access токена. Пример: `Bearer <token>`',
            'schema': {
                'type': 'string'
            }
        }
    ]
})
@jwt_required(refresh=True)
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
@swag_from({
    'responses': {
        201: {
            'description': 'Пользователь зарегистрирован'
        },
        400: {
            'description': 'Данные для регистрации не прошли проверку'
        },
        403: {
            'description': 'Авторизованный пользователь пытается получить доступ'
        }
    },
    'parameters': [
        {
            'name': 'user_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'login': {
                        'type': 'string',
                        'maxLength': 30,
                        'description': 'Логин пользователя, не более 30 символов'
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Email пользователя'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Введенный пароль'
                    },
                    'password_repeat': {
                        'type': 'string',
                        'description': 'Повторный ввод пароля'
                    },
                },
                'required': ['login', 'email', 'password', 'password_repeat']
            }
        }
    ]
})
@anonymous_required
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
        "refresh_token": refresh_token
    }), 201


@accounting_bp.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Пользователь успешно вошёл'
        },
        400: {
            'description': 'Данные для авторизации не прошли проверку'
        },
        403: {
            'description': 'Авторизованный пользователь пытается получить доступ'
        }
    },
    'parameters': [
        {
            'name': 'user_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Email пользователя'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Введенный пароль'
                    }
                },
                'required': ['email', 'password']
            }
        }
    ]
})
@anonymous_required
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
                        "refresh_token": refresh_token
        }), 200

    return jsonify({"success": False,
        "message": "Неверная информация в полях авторизации"}), 400


@accounting_bp.route('/profile', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все данные пользователя'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        }
    },
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'description': 'JWT access токен для доступа. Пример: `Bearer <token>`',
            'schema': {
                'type': 'string'
            }
        }
    ]
})
@jwt_required()
def show_profile():
    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    user_schema = UserSchema(unknown=EXCLUDE)
    return jsonify({"user": user_schema.dump(current_user)}), 200


@accounting_bp.route('/edit_email', methods=['PUT'])
@swag_from({
    'responses': {
        200: {
            'description': 'Email успешно изменён'
        },
        400: {
            'description': 'Неверные данные для изменения email'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        }
    },
    'parameters': [
        {
            'name': 'user_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Новый email пользователя'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Введенный пароль'
                    }
                },
                'required': ['email', 'password']
            }
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'description': 'JWT access токен для доступа. Пример: `Bearer <token>`',
            'schema': {
                'type': 'string'
            }
        }
    ]
})
@jwt_required()
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
@swag_from({
    'responses': {
        200: {
            'description': 'Логин успешно изменён'
        },
        400: {
            'description': 'Неверные данные для изменения логина'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        }
    },
    'parameters': [
        {
            'name': 'user_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'new_login': {
                        'type': 'string',
                        'maxLength': 30,
                        'description': 'Новый логин пользователя, не более 30 символов'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Введенный пароль'
                    }
                },
                'required': ['new_login']
            }
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'description': 'JWT access токен для доступа. Пример: `Bearer <token>`',
            'schema': {
                'type': 'string'
            }
        }
    ]
})
@jwt_required()
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
@swag_from({
    'responses': {
        200: {
            'description': 'Пароль успешно изменён'
        },
        400: {
            'description': 'Неверные данные для изменения пароля'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        }
    },
    'parameters': [
        {
            'name': 'user_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'old_password': {
                        'type': 'string',
                        'description': 'Старый пароль'
                    },
                    'new_password': {
                        'type': 'string',
                        'description': 'Новый пароль'
                    }
                },
                'required': ['old_password', 'new_password']
            }
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'description': 'JWT access токен для доступа. Пример: `Bearer <token>`',
            'schema': {
                'type': 'string'
            }
        }
    ]
})
@jwt_required()
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
