from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError, EXCLUDE

from webapp import db
from webapp.models.Category import Category
from webapp.models.Country import Country
from webapp.models.SpecialOffer import SpecialOffer
from webapp.models.Tour import Tour
from webapp.models.User import User
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema
from webapp.schemas.OfferSchema import OfferSchema
from webapp.schemas.RegistrationSchema import RegistrationSchema
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
    tours_schema = TourSchema(many=True,  exclude=("tour_replies","tour_text", "tour_description", "tour_price",
                                                   "tour_start_date", "tour_end_date", "offers", "price_with_discount"))
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
                    },
                    'offer_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID акции на тур, необязательно для заполнения'
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
    offer_id = json_data.get("offer_id")

    try:
        valid_category_uuid = UUID(category_id)
        valid_country_uuid = UUID(country_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()
        country = Country.query.filter_by(country_id=valid_country_uuid).first()
        offer = None
        if offer_id:
            valid_offer_uuid = UUID(offer_id)
            offer = SpecialOffer.query.filter_by(offer_id=valid_offer_uuid).first()
            if not offer:
                return jsonify({"success": False,
                                "message": "Акция с переданным UUID не найдена"}), 400
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории, страны или акции'}), 400

    if not category:
        return jsonify({"success": False,
                        "message": "Категория с переданным UUID не найдена"}), 400

    if not country:
        return jsonify({"success": False,
                        "message": "Страна с переданным UUID не найдена"}), 400

    tour_schema = TourSchema(unknown=EXCLUDE, exclude=("tour_replies",))

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
    if offer:
        tour.offers.append(offer)
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

        tour_schema = TourSchema(exclude=("tour_replies",))

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
                    },
                    'offer_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID акции на тур, необязательно для заполнения'
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
    offer_id = json_data.get("offer_id")

    try:
        valid_category_uuid = UUID(category_id)
        valid_country_uuid = UUID(country_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()
        country = Country.query.filter_by(country_id=valid_country_uuid).first()
        offer = None
        if offer_id:
            valid_offer_uuid = UUID(offer_id)
            offer = SpecialOffer.query.filter_by(offer_id=valid_offer_uuid).first()
            if not offer:
                return jsonify({"success": False,
                                "message": "Акция с переданным UUID не найдена"}), 400
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

    tour_schema = TourSchema(unknown=EXCLUDE, exclude=("tour_replies",))

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

    if tour.offers.first() != offer:
        for special_offer in tour.offers.all():
            tour.offers.remove(special_offer)
        if offer_id:
            tour.offers.append(offer)

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

        tour_schema = TourSchema(exclude=("tour_replies","tour_text", "offers"))

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


@admin_bp.route("/offers/new", methods=["POST"])
@swag_from({
    'responses': {
        201: {
            'description': 'Создана новая скидка'
        },
        400: {
            'description': 'Данные для создания новой скидки не прошли проверку'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        }
    },
    'parameters': [
        {
            'name': 'special_offer',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'offer_title': {
                        'type': 'string',
                        'maxLength': 50,
                        'description': 'Название скидки, не более 50 символов'
                    },
                    'discount_size': {
                        'type': 'number',
                        'format': 'integer',
                        'description': 'Процент скидки, обязательно для заполнения'
                    },
                    'end_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Дата окончания действия скидки, обязательно для заполнения'
                    },
                },
                'required': ['offer_title', 'discount_size', 'end_date']
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
def add_special_offer():
    """
       Добавляет новую скидку
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    json_data = request.get_json()

    offer_schema = OfferSchema(unknown=EXCLUDE)

    try:
        special_offer = offer_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    db.session.add(special_offer)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Скидка успешно создана!",
        "special_offer": offer_schema.dump(special_offer)
    }), 201


@admin_bp.route("/offers/<string:offer_id>/edit", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этой скидке'
        },
        400: {
            'description': 'Неверный формат UUID скидки'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если скидки с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'offer_id',
            'description': 'ID скидки',
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
def show_special_offer_edit_page(offer_id: str):
    """
       Возвращает всю информацию про конкретную скидку для формы редактирования
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_offer_uuid = UUID(offer_id)

        offer = SpecialOffer.query.filter_by(offer_id=valid_offer_uuid).first()

        if not offer:
            return jsonify({"success": False,
                "message": "Скидка с таким ID не найдена"}), 404

        offer_schema = OfferSchema()

        offer_data = offer_schema.dump(offer)

        return jsonify({"success": True,
            "special_offer": offer_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у скидки'}), 400


@admin_bp.route("/offers/<string:offer_id>/edit", methods=["PUT"])
@swag_from({
    'responses': {
        200: {
            'description': 'Данные скидки обновлены'
        },
        400: {
            'description': 'Данные для обновления скидки не прошли проверку или неверный формат UUID скидки'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если скидки с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'offer_id',
            'description': 'ID скидки',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'special_offer',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'offer_title': {
                        'type': 'string',
                        'maxLength': 50,
                        'description': 'Название скидки, не более 50 символов'
                    },
                    'discount_size': {
                        'type': 'number',
                        'format': 'integer',
                        'description': 'Процент скидки, обязательно для заполнения'
                    },
                    'end_date': {
                        'type': 'string',
                        'format': 'date',
                        'description': 'Дата окончания действия скидки, обязательно для заполнения'
                    },
                },
                'required': ['offer_title', 'discount_size', 'end_date']
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
def edit_special_offer(offer_id: str):
    """
       Обновляет данные скидки
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_offer_uuid = UUID(offer_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у скидки'}), 400

    json_data = request.get_json()

    offer = SpecialOffer.query.filter_by(offer_id=valid_offer_uuid).first()

    if not offer:
        return jsonify({"success": False,
            "message": "Скидка с таким ID не найдена"}), 404

    offer_schema = OfferSchema(unknown=EXCLUDE)

    try:
        update_data = offer_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    for key, value in json_data.items():
        setattr(offer, key, value)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные скидки успешно изменены!",
        "special_offer": offer_schema.dump(offer)
    }), 200


@admin_bp.route("/offers/<string:offer_id>/delete", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этой скидке'
        },
        400: {
            'description': 'Неверный формат UUID скидки'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если скидки с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'offer_id',
            'description': 'ID скидки',
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
def show_special_offer_delete_page(offer_id: str):
    """
       Возвращает всю информацию про конкретную скидку для страницы удаления
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_offer_uuid = UUID(offer_id)

        offer = SpecialOffer.query.filter_by(offer_id=valid_offer_uuid).first()

        if not offer:
            return jsonify({"success": False,
                "message": "Скидка с таким ID не найдена"}), 404

        offer_schema = OfferSchema()

        offer_data = offer_schema.dump(offer)

        return jsonify({"success": True,
            "special_offer": offer_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у скидки'}), 400


@admin_bp.route("/offers/<string:offer_id>/delete", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Скидка успешно удалена'
        },
        400: {
            'description': 'Поле с согласием не отмечено или неверный формат UUID скидки'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если скидки с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'offer_id',
            'description': 'ID скидки',
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
def delete_special_offer(offer_id: str):
    """
       Удаляет выбранную скидку
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_offer_uuid = UUID(offer_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у скидки'}), 400

    json_data = request.get_json()
    acceptance = json_data.get('acceptance')

    offer = SpecialOffer.query.filter_by(offer_id=valid_offer_uuid).first()

    if not offer:
        return jsonify({"success": False,
            "message": "Скидка с таким ID не найдена"}), 404

    if acceptance is None or acceptance is False:
        return jsonify({"success": False,
            "message": "Если вы хотите удалить данную скидку, "
                                   "вам необходимо поставить галочку выше"}), 400

    db.session.delete(offer)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Скидка успешно удалена!"}), 200


@admin_bp.route('/moderator_registration', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Аккаунт модератора создан'
        },
        400: {
            'description': 'Данные для регистрации не прошли проверку'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        }
    },
    'parameters': [
        {
            'name': 'moderator_data',
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
def registrate_moderator():
    """
       Создание аккаунтов для модераторов
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

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
    new_user.set_moderator_role()

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Аккаунт модератора успешно зарегистрирован!",
    }), 201
