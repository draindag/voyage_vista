from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy import func

from webapp import db
from webapp.models.Category import Category
from webapp.models.Review import Review
from webapp.models.Tour import Tour
from webapp.models.Country import Country
from webapp.models.User import User
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema
from webapp.schemas.ReviewSchema import ReviewSchema
from webapp.schemas.TourSchema import TourSchema

tours_bp = Blueprint("tours", __name__)


@tours_bp.route("/categories", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все категории'
        }
    }
})
def show_categories():
    """
       Возвращает все категории для туров
       ---
       """

    categories = Category.query.all()
    categories_schema = CategorySchema(many=True)
    categories_data = categories_schema.dump(categories)

    return jsonify({"success": True,
                    "categories": categories_data}), 200


@tours_bp.route("/special_offers", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все туры с акциями'
        }
    }
})
def show_tours_with_discounts():
    """
       Возвращает все туры, у которых есть какие-нибудь акции
       ---
       """

    tours_with_discounts = db.session.query(Tour).filter(Tour.offers.any()).all()
    tours_schema = TourSchema(many=True)
    discounts_tours_data = tours_schema.dump(tours_with_discounts)

    return jsonify({"success": True,
                    "tours": discounts_tours_data}), 200


@tours_bp.route("/popular", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул 30 туров с высокой оценкой'
        }
    }
})
def show_most_popular_tours():
    """
       Возвращает первые 30 туров с самой высокой оценкой
       ---
       """

    popular_tours = db.session.query(Tour).outerjoin(Tour.reviews).group_by(Tour.tour_id).order_by(
        func.coalesce(func.avg(Review.review_value), 0).desc()).limit(30).all()
    tours_schema = TourSchema(many=True)
    popular_tours_data = tours_schema.dump(popular_tours)

    return jsonify({"success": True,
                    "tours": popular_tours_data}), 200


@tours_bp.route("/categories/<string:category_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все туры для этой категории'
        },
        400: {
            'description': 'Неверный формат uuid'
        },
        404: {
            'description': 'Если категории с таким id нет'
        }
    },
    'parameters': [
        {
            'name': 'category_id',
            'description': 'ID категории',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
def show_category_page(category_id: str):
    """
           Возвращает все туры, относящиеся к данной категории
           ---
           """

    try:
        valid_category_uuid = UUID(category_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()

        if not category:
            return jsonify({"success": False,
                "message": "Категория не найдена"}), 404

        tours_for_category = category.tours
        tours_schema = TourSchema(many=True)
        tours_for_category_data = tours_schema.dump(tours_for_category)

        return jsonify({"success": True,
                        "tours": tours_for_category_data}), 200

    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории'}), 400


@tours_bp.route("/categories/<string:category_id>/<string:tour_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этому туру'
        },
        400: {
            'description': 'Неверный формат uuid у одного из параметров'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если категории или тура с таким id нет'
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
        },
        {
            'name': 'category_id',
            'description': 'ID категории',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
@jwt_required()
def show_tour_page_from_category(category_id: str, tour_id: str):
    """
       Возвращает всю информацию про конкретный тур
       ---
       """
    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_category_uuid = UUID(category_id)
        valid_tour_uuid = UUID(tour_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()

        if not category:
            return jsonify({"success": False,
                            "message": "Категория не найдена"}), 404

        tour = category.tours.filter_by(tour_id=valid_tour_uuid).first()

        if not tour:
            return jsonify({"success": False,
                "message": "Тур не найден"}), 404

        tour_schema = TourSchema()
        tour_data = tour_schema.dump(tour)

        return jsonify({"success": True,
            "tour": tour_data}), 200

    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории или тура'}), 400


@tours_bp.route("/countries/<string:country_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этой стране'
        },
        400: {
            'description': 'Неверный формат uuid'
        },
        404: {
            'description': 'Если страны с таким id нет'
        }
    },
    'parameters': [
        {
            'name': 'country_id',
            'description': 'ID страны',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
def show_country_page(country_id: str):
    """
        Возвращает всю информацию про конкретную страну
       ---
       """

    try:
        valid_country_uuid = UUID(country_id)
        country = Country.query.filter_by(country_id=valid_country_uuid).first()

        if not country:
            return jsonify({"success": False,
                    "message": "Страна не найдена"}), 404

        country_schema = CountrySchema()
        country_data = country_schema.dump(country)

        return jsonify({"success": True,
                        "country": country_data}), 200

    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у страны'}), 400

@tours_bp.route("/countries/<string:country_id>/<string:tour_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этому туру'
        },
        400: {
            'description': 'Неверный формат uuid у одного из параметров'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если страны или тура с таким id нет'
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
        },
        {
            'name': 'country_id',
            'description': 'ID страны',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
@jwt_required()
def show_tour_page_from_country(country_id: str, tour_id: str):
    """
       Возвращает всю информацию про конкретный тур
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_country_uuid = UUID(country_id)
        valid_tour_uuid = UUID(tour_id)
        country = Country.query.filter_by(country_id=valid_country_uuid).first()

        if not country:
            return jsonify({"success": False,
                    "message": "Страна не найдена"}), 404

        tour = country.tours.filter_by(tour_id=valid_tour_uuid).first()

        if not tour:
            return jsonify({"success": False,
                            "message": "Тур не найден"}), 404

        tour_schema = TourSchema()
        tour_data = tour_schema.dump(tour)

        return jsonify({"success": True,
                        "tour": tour_data}), 200

    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у страны или тура'}), 400


@tours_bp.route('/<string:tour_id>/to_favourite', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Добавил тур в избранное пользователя'
        },
        400: {
            'description': 'Неверный формат uuid'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если тура с таким id нет'
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
        },
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
@jwt_required()
def add_tour_to_favourites(tour_id: str):
    """
        Добавляет тур в избранное пользователя
        ---
        """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
                        "message": "Тур не найден"}), 404

    current_user.fav_tours.append(tour)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Тур успешно добавлен в избранное"}), 201


@tours_bp.route("/<string:tour_id>/out_of_favourite", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Удалил тур из избранного пользователя'
        },
        400: {
            'description': 'Неверный формат uuid'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если тура с таким id нет'
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
        },
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
@jwt_required()
def unfavourite_tour(tour_id: str):
    """
        Удаляет тур из избранного пользователя
        ---
        """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у тура'}), 400

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
                        "message": "Тур не найден"}), 404

    current_user.fav_tours.remove(tour)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Тур успешно удален из избранного"}), 200


@tours_bp.route('/<string:tour_id>/payment', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по туру для совершения оплаты'
        },
        400: {
            'description': 'Неверный формат uuid'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если тура с таким id нет'
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
        },
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
@jwt_required()
def show_tour_payment_info(tour_id: str):
    """
        Возвращает данные тура для совершения оплаты
        ---
        """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у тура'}), 400

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
                        "message": "Тур не найден"}), 404

    tour_schema = TourSchema()
    tour_data = tour_schema.dump(tour)

    return jsonify({"success": True,
                    "tour": tour_data}), 200


@tours_bp.route('/<string:tour_id>/payment', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Сохранил информацию об оплате тура пользователем'
        },
        400: {
            'description': 'Неверный формат uuid'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если тура с таким id нет'
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
        },
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
        }
    ]
})
@jwt_required()
def add_transaction(tour_id: str):
    """
        Фиксирует проведение оплаты за тур
        ---
        """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у тура'}), 400

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
                        "message": "Тур не найден"}), 404

    json_data = request.get_json()
    acceptance = json_data.get('acceptance')

    if acceptance is None or acceptance is False:
        return jsonify({"success": False,
            "message": "Для совершения оплаты, вам необходимо поставить галочку выше"}), 400

    current_user.transactions.append(tour)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Оплата прошла успешно!"}), 200


@tours_bp.route('/<string:tour_id>/add_review', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Добавил отзыв на тур'
        },
        400: {
            'description': 'Данные тура не прошли проверку или неверный формат uuid'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку'
        },
        404: {
            'description': 'Если тура с таким id нет'
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
        },
        {
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'review',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'review_text': {
                        'type': 'string',
                        'description': 'Текст отзыва, обязательно для заполнения'
                    },
                    'review_value': {
                        'type': 'number',
                        'format': 'integer',
                        'description': 'Оценка тура, обязательно для заполнения'
                    }
                },
                'required': ['review_text', 'review_value']
            }
        }
    ]
})
@jwt_required()
def add_review_to_tour(tour_id: str):
    """
        Оставляет отзыв на тур
        ---
        """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401

    try:
        valid_tour_uuid = UUID(tour_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400

    tour = Tour.query.filter_by(tour_id=valid_tour_uuid).first()

    if not tour:
        return jsonify({"success": False,
                        "message": "Тур не найден"}), 404

    json_data = request.get_json()
    json_data['author_id'] = current_user.user_id
    json_data['tour_id'] = tour_id
    review_schema = ReviewSchema(unknown=EXCLUDE)

    try:
        review = review_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                        "errors": err.messages}), 400

    db.session.add(review)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Отзыв успешно сохранён!",
                    "review": review_schema.dump(review)}), 201
