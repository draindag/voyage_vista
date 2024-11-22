from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError, EXCLUDE

from webapp import db
from webapp.models.Category import Category
from webapp.models.Country import Country
from webapp.models.Tour import Tour
from webapp.models.User import User
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema
from webapp.schemas.TourSchema import TourSchema

admin_bp = Blueprint("admin_panel", __name__)

@admin_bp.route("/categories", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все имеющиеся категории'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
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
def show_categories_for_admin():
    """
       Возвращает все категории для панели админа
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                "message": "Неизвестный пользователь!"}), 401

    categories = Category.query.all()
    categories_schema = CategorySchema(many=True)
    categories_data = categories_schema.dump(categories)
    return jsonify(categories_data), 200


@admin_bp.route("/countries", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все имеющиеся туры'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
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
def show_countries_for_admin():
    """
       Возвращает все страны для панели админа
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    countries = Country.query.all()
    countries_schema = CountrySchema(many=True)
    countries_data = countries_schema.dump(countries)
    return jsonify(countries_data), 200


@admin_bp.route("/tours", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все имеющиеся туры'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
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
def show_tours_for_admin():
    """
       Возвращает все туры для панели админа
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    tours = Tour.query.all()
    tours_schema = TourSchema(many=True)
    tours_data = tours_schema.dump(tours)
    return jsonify(tours_data), 200


@admin_bp.route("/categories/new", methods=["POST"])
@swag_from({
    'responses': {
        201: {
            'description': 'Создана новая категория'
        },
        400: {
            'description': 'Данные для создания новой категории не прошли проверку'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        }
    },
    'parameters': [
        {
            'name': 'category',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'category_title': {
                        'type': 'string',
                        'maxLength': 30,
                        'description': 'Название категории, не более 30 символов'
                    },
                    'category_description': {
                        'type': 'string',
                        'description': 'Описание категории'
                    }
                },
                'required': ['category_title', 'category_description']
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
def add_category():
    """
       Добавляет новую категорию
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    json_data = request.get_json()

    category_exists = Category.query.filter_by(category_title=json_data.get("category_title")).first()
    if category_exists:
        return {"success": False,
                "message": "Категория с таким названием уже существует"}, 400

    category_schema = CategorySchema(unknown=EXCLUDE)

    try:
        category = category_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Категория успешно добавлена!",
        "category": category_schema.dump(category)
    }), 201



@admin_bp.route("/categories/<string:category_id>/edit", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этой категории'
        },
        400: {
            'description': 'Неверный формат UUID категории'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если категории с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'category_id',
            'description': 'ID категории',
            'in': 'path',
            'type': 'string',
            'required': True
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
def show_category_edit_page(category_id: str):
    """
       Возвращает всю информацию про конкретную категорию для формы редактирования
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_category_uuid = UUID(category_id)

        category = Category.query.filter_by(category_id=valid_category_uuid).first()

        if not category:
            return jsonify({"success": False,
                "message": "Категория с таким ID не найдена"}), 404

        category_schema = CategorySchema()

        category_data = category_schema.dump(category)

        return jsonify({"success": True,
            "category": category_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у категории'}), 400


@admin_bp.route("/categories/<string:category_id>/edit", methods=["PUT"])
@swag_from({
    'responses': {
        200: {
            'description': 'Данные категории обновлены'
        },
        400: {
            'description': 'Данные для обновления категории не прошли проверку или неверный формат UUID категории'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если категории с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'category_id',
            'description': 'ID категории',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'category',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'category_title': {
                        'type': 'string',
                        'maxLength': 30,
                        'description': 'Название категории, не более 30 символов'
                    },
                    'category_description': {
                        'type': 'string',
                        'description': 'Описание категории'
                    }
                },
                'required': ['category_title', 'category_description']
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
def edit_category(category_id: str):
    """
       Обновляет данные категории
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_category_uuid = UUID(category_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у категории'}), 400

    json_data = request.get_json()

    category = Category.query.filter_by(category_id=valid_category_uuid).first()

    if not category:
        return jsonify({"success": False,
            "message": "Категория с таким ID не найдена"}), 404

    if category.category_title != json_data.get("category_title"):
        category_exists = Category.query.filter_by(category_title=json_data.get("category_title")).first()
        if category_exists:
            return jsonify({"success": False,
                    "message": "Категория с таким названием уже существует"}), 400

    category_schema = CategorySchema(unknown=EXCLUDE)

    try:
        update_data = category_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    for key, value in json_data.items():
        setattr(category, key, value)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные категории успешно изменены!",
        "category": category_schema.dump(category)
    }), 200


@admin_bp.route("/categories/<string:category_id>/delete", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этой категории'
        },
        400: {
            'description': 'Неверный формат UUID категории'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если категории с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'category_id',
            'description': 'ID категории',
            'in': 'path',
            'type': 'string',
            'required': True
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
def show_category_delete_page(category_id: str):
    """
       Возвращает всю информацию про конкретную категорию для страницы удаления
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_category_uuid = UUID(category_id)

        category = Category.query.filter_by(category_id=valid_category_uuid).first()

        if not category:
            return jsonify({"success": False,
                "message": "Категория с таким ID не найдена"}), 404

        category_schema = CategorySchema()

        category_data = category_schema.dump(category)

        return jsonify({"success": True,
            "category": category_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у категории'}), 400


@admin_bp.route("/categories/<string:category_id>/delete", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Категория успешно удалена'
        },
        400: {
            'description': 'Поле с согласием не отмечено или неверный формат UUID категории'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если категории с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'category_id',
            'description': 'ID категории',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'acceptance',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'acceptance': {
                        'type': 'boolean'
                    }
                }
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
def delete_category(category_id: str):
    """
       Удаляет выбранную категорию
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_category_uuid = UUID(category_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у категории'}), 400

    json_data = request.get_json()
    acceptance = json_data.get('acceptance')

    category = Category.query.filter_by(category_id=valid_category_uuid).first()

    if not category:
        return jsonify({"success": False,
            "message": "Категория с таким ID не найдена"}), 404

    if acceptance is None or acceptance is False:
        return jsonify({"success": False,
            "message": "Если вы хотите удалить данную категорию, "
                                   "вам необходимо поставить галочку выше"}), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Категория успешно удалена!"}), 200


@admin_bp.route("/countries/new", methods=["POST"])
@swag_from({
    'responses': {
        201: {
            'description': 'Добавлена новая страна'
        },
        400: {
            'description': 'Данные для добавления новой страны не прошли проверку'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        }
    },
    'parameters': [
        {
            'name': 'country',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'country_name': {
                        'type': 'string',
                        'maxLength': 30,
                        'description': 'Название страны, не более 30 символов'
                    },
                    'country_description': {
                        'type': 'string',
                        'description': 'Описание страны'
                    }
                },
                'required': ['country_name', 'country_description']
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
def add_country():
    """
       Добавляет новую страну
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    json_data = request.get_json()

    country_exists = Country.query.filter_by(country_name=json_data.get("country_name")).first()
    if country_exists:
        return jsonify({"success": False,
                "message": "Страна с таким названием уже существует"}), 400

    country_schema = CountrySchema(unknown=EXCLUDE)

    try:
        country = country_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    db.session.add(country)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Страна успешно добавлена!",
        "country": country_schema.dump(country)
    }), 201


@admin_bp.route("/countries/<string:country_id>/edit", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по данной стране'
        },
        400: {
            'description': 'Неверный формат UUID страны'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если страны с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'country_id',
            'description': 'ID страны',
            'in': 'path',
            'type': 'string',
            'required': True
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
def show_country_edit_page(country_id: str):
    """
       Возвращает всю информацию про конкретную страну для формы редактирования
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_country_id_uuid = UUID(country_id)

        country = Country.query.filter_by(country_id=valid_country_id_uuid).first()

        if not country:
            return jsonify({"success": False,
                "message": "Страна с таким ID не найдена"}), 404

        country_schema = CountrySchema()

        country_data = country_schema.dump(country)

        return jsonify({"success": True,
            "country": country_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у страны'}), 400


@admin_bp.route("/countries/<string:country_id>/edit", methods=["PUT"])
@swag_from({
    'responses': {
        200: {
            'description': 'Данные страны обновлены'
        },
        400: {
            'description': 'Данные для обновления страны не прошли проверку или неверный формат UUID страны'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если страны с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'country_id',
            'description': 'ID страны',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'country',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'country_name': {
                        'type': 'string',
                        'maxLength': 30,
                        'description': 'Название страны, не более 30 символов'
                    },
                    'country_description': {
                        'type': 'string',
                        'description': 'Описание страны'
                    }
                },
                'required': ['country_name', 'country_description']
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
def edit_country(country_id: str):
    """
       Обновляет данные страны
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_country_uuid = UUID(country_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у страны'}), 400

    json_data = request.get_json()

    country = Country.query.filter_by(country_id=valid_country_uuid).first()

    if not country:
        return jsonify({"success": False,
            "message": "Страна с таким ID не найдена"}), 404

    if country.country_name != json_data.get("country_name"):
        country_exists = Country.query.filter_by(country_name=json_data.get("country_name")).first()
        if country_exists:
            return jsonify({"success": False,
                    "message": "Страна с таким названием уже существует"}), 400

    country_schema = CountrySchema(unknown=EXCLUDE)

    try:
        update_data = country_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    for key, value in json_data.items():
        setattr(country, key, value)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные страны успешно изменены!",
        "category": country_schema.dump(country)
    }), 200


@admin_bp.route("/countries/<string:country_id>/delete", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по данной стране'
        },
        400: {
            'description': 'Неверный формат UUID страны'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если страны с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'country_id',
            'description': 'ID страны',
            'in': 'path',
            'type': 'string',
            'required': True
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
def show_country_delete_page(country_id: str):
    """
       Возвращает всю информацию про конкретную страну для страницы удаления
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_country_uuid = UUID(country_id)

        country = Country.query.filter_by(country_id=valid_country_uuid).first()

        if not country:
            return jsonify({"success": False,
                "message": "Страна с таким ID не найдена"}), 404

        country_schema = Country()

        country_data = country_schema.dump(country)

        return jsonify({"success": True,
            "country": country_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у страны'}), 400


@admin_bp.route("/countries/<string:country_id>/delete", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Страна успешно удалена'
        },
        400: {
            'description': 'Поле с согласием не отмечено или неверный формат UUID страны'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если страны с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'country_id',
            'description': 'ID страны',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'acceptance',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'acceptance': {
                        'type': 'boolean'
                    }
                }
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
def delete_country(country_id: str):
    """
       Удаляет выбранную страну
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_country_uuid = UUID(country_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у страны'}), 400

    json_data = request.get_json()
    acceptance = json_data.get('acceptance')

    country = Country.query.filter_by(country_id=valid_country_uuid).first()

    if not country:
        return jsonify({"success": False,
            "message": "Страна с таким ID не найдена"}), 404

    if acceptance is None or acceptance is False:
        return jsonify({"success": False,
            "message": "Если вы хотите удалить данную страну, "
                                   "вам необходимо поставить галочку выше"}), 400

    db.session.delete(country)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Страна успешно удалена!"}), 200


@admin_bp.route("/tours/new", methods=["POST"])
@swag_from({
    'responses': {
        201: {
            'description': 'Добавлен новый тур'
        },
        400: {
            'description': 'Данные для добавления нового тура не прошли проверку'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        }
    },
    'parameters': [
        {
            'name': 'tour',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'tour_title': {
                        'type': 'string',
                        'maxLength': 40,
                        'description': 'Название тура, не более 40 символов'
                    },
                    'tour_description': {
                        'type': 'string',
                        'description': 'Описание тура, не более 50 символов'
                    },
                    'tour_text': {
                        'type': 'string',
                        'description': 'Текст тура, обязательно для заполнения'
                    },
                    'tour_price': {
                        'type': 'number',
                        'format': 'decimal',
                        'description': 'Цена тура, обязательно для заполнения'
                    },
                    'tour_start_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Дата начала тура, обязательно для заполнения'
                    },
                    'tour_end_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Дата окончания тура, обязательно для заполнения'
                    },
                    'category_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID категории тура, обязательно для заполнения'
                    },
                    'country_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID страны тура, обязательно для заполнения'
                    }
                },
                'required': ['tour_title', 'tour_description', 'tour_text',
                             'tour_price', 'tour_start_date', 'tour_end_date',
                             'category_id', 'country_id']
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
def add_tour():
    """
       Добавляет новый тур
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    json_data = request.get_json()
    tour_title = json_data.get("tour_title")
    category_id = json_data.get("category_id")
    country_id = json_data.get("country_id")

    try:
        valid_category_uuid = UUID(category_id)
        valid_country_uuid = UUID(country_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()
        country = Country.query.filter_by(country_id=valid_country_uuid).first()
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории или страны'}), 400

    if not category:
        return jsonify({"success": False,
                        "message": "Категория с переданным UUID не найдена"}), 400

    if not country:
        return jsonify({"success": False,
                        "message": "Страна с переданным UUID не найдена"}), 400

    tour_schema = TourSchema(unknown=EXCLUDE)

    try:
        tour = tour_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                "errors": err.messages}), 400

    tour_exists_in_that_category = Tour.query.filter_by(tour_title=tour_title, category_id=category_id).first()
    if tour_exists_in_that_category:
        return jsonify({"success": False,
                "message": "Тур с таким названием уже существует в этой категории"}), 400

    db.session.add(tour)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Тур успешно добавлен!",
        "tour": tour_schema.dump(tour)
    }), 201


@admin_bp.route("/tours/<string:tour_id>/edit", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по данному туру'
        },
        400: {
            'description': 'Неверный формат UUID тура'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если тура с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
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
def show_tour_edit_page(tour_id: str):
    """
       Возвращает всю информацию про конкретный тур для формы редактирования
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_tour_id_uuid = UUID(tour_id)

        tour = Tour.query.filter_by(tour_id=valid_tour_id_uuid).first()

        if not tour:
            return jsonify({"success": False,
                "message": "Тур с таким ID не найден"}), 404

        tour_schema = TourSchema()

        tour_data = tour_schema.dump(tour)

        return jsonify({"success": True,
            "tour": tour_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400


@admin_bp.route("/tours/<string:tour_id>/edit", methods=["PUT"])
@swag_from({
    'responses': {
        200: {
            'description': 'Данные тура обновлены'
        },
        400: {
            'description': 'Данные для обновления тура не прошли проверку или неверный формат UUID тура'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если тура с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tour',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'tour_title': {
                        'type': 'string',
                        'maxLength': 40,
                        'description': 'Название тура, не более 40 символов'
                    },
                    'tour_description': {
                        'type': 'string',
                        'description': 'Описание тура, не более 50 символов'
                    },
                    'tour_text': {
                        'type': 'string',
                        'description': 'Текст тура, обязательно для заполнения'
                    },
                    'tour_price': {
                        'type': 'number',
                        'format': 'decimal',
                        'description': 'Цена тура, обязательно для заполнения'
                    },
                    'tour_start_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Дата начала тура, обязательно для заполнения'
                    },
                    'tour_end_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Дата окончания тура, обязательно для заполнения'
                    },
                    'category_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID категории тура, обязательно для заполнения'
                    },
                    'country_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID страны тура, обязательно для заполнения'
                    }
                },
                'required': ['tour_title', 'tour_description', 'tour_text',
                             'tour_price', 'tour_start_date', 'tour_end_date',
                             'category_id', 'country_id']
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
def edit_tour(tour_id: str):
    """
       Обновляет данные тура
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400

    json_data = request.get_json()
    tour_title = json_data.get("tour_title")
    category_id = json_data.get("category_id")
    country_id = json_data.get("country_id")

    try:
        valid_category_uuid = UUID(category_id)
        valid_country_uuid = UUID(country_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()
        country = Country.query.filter_by(country_id=valid_country_uuid).first()
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории или страны'}), 400

    if not category:
        return jsonify({"success": False,
                        "message": "Категория с переданным UUID не найдена"}), 400

    if not country:
        return jsonify({"success": False,
                        "message": "Страна с переданным UUID не найдена"}), 400

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
            "message": "Страна с таким ID не найдена"}), 404

    tour_schema = TourSchema(unknown=EXCLUDE)

    try:
        update_data = tour_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    if tour.tour_title != tour_title:
        tour_exists = Tour.query.filter_by(tour_title=tour_title, category_id=category_id).first()
        if tour_exists:
            return jsonify({"success": False,
                    "message": "Тур с таким названием уже существует в этой категории"}), 400

    for key, value in json_data.items():
        setattr(tour, key, value)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные тура успешно изменены!",
        "tour": tour_schema.dump(tour)
    }), 200


@admin_bp.route("/tours/<string:tour_id>/delete", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по данному туру'
        },
        400: {
            'description': 'Неверный формат UUID тура'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если тура с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
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
def show_tour_delete_page(tour_id: str):
    """
       Возвращает всю информацию про конкретный тур для страницы удаления
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)

        tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

        if not tour:
            return jsonify({"success": False,
                "message": "Тур с таким ID не найден"}), 404

        tour_schema = TourSchema()

        tour_data = tour_schema.dump(tour)

        return jsonify({"success": True,
            "tour": tour_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400


@admin_bp.route("/tours/<string:tour_id>/delete", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Тур успешно удалён'
        },
        400: {
            'description': 'Поле с согласием не отмечено или неверный формат UUID тура'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если тура с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'acceptance',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'acceptance': {
                        'type': 'boolean'
                    }
                }
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
def delete_tour(tour_id: str):
    """
       Удаляет выбранный тур
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400

    json_data = request.get_json()
    acceptance = json_data.get('acceptance')

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
            "message": "Тур с таким ID не найден"}), 404

    if acceptance is None or acceptance is False:
        return jsonify({"success": False,
            "message": "Если вы хотите удалить данный тур, "
                                   "вам необходимо поставить галочку выше"}), 400

    db.session.delete(tour)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Тур успешно удалён!"}), 200
