import os
from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy import func

from webapp import db
from webapp.models.Category import Category
from webapp.models.Reply import Reply
from webapp.models.Review import Review
from webapp.models.Tour import Tour
from webapp.models.Country import Country
from webapp.models.User import User
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.ReplySchema import ReplySchema
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
            'description': 'Вернул все туры с акциями постранично'
        }
    },
    'parameters': [
        {
            'name': 'page',
            'type': 'integer',
            'required': False,
            'description': 'Номер страницы для пагинации (по умолчанию 1)',
            'in': 'query'
        }
    ]
})
def show_tours_with_discounts():
    """
       Возвращает все туры, у которых есть какие-нибудь акции постранично
       ---
       """

    page = request.args.get('page', 1, type=int)
    tours_with_discounts = db.session.query(Tour).filter(Tour.offers.any()).paginate(
        page=page, per_page=int(os.getenv("TOURS_PER_PAGE")), error_out=False)
    tours_schema = TourSchema(many=True, exclude=("tour_text",))
    discounts_tours_data = tours_schema.dump(tours_with_discounts)

    return jsonify({"success": True,
                    "tours": discounts_tours_data,
                    "prev_page": tours_with_discounts.has_prev,
                    "next_page": tours_with_discounts.has_next}), 200


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

    page = request.args.get('page', 1, type=int)
    page_size = int(os.getenv("TOURS_PER_PAGE"))
    popular_tours = (
        db.session.query(Tour)
        .outerjoin(Tour.reviews)
        .group_by(Tour.tour_id)
        .order_by(func.coalesce(func.avg(Review.review_value), 0).desc())
        .limit(20)
        .all()
    )
    offset = (page - 1) * page_size
    has_prev = page > 1
    has_next = (page * page_size) < len(popular_tours)
    paginated_tours = popular_tours[offset:offset + page_size]
    tours_schema = TourSchema(many=True, exclude=("tour_text",))
    popular_tours_data = tours_schema.dump(paginated_tours)

    return jsonify({"success": True,
                    "tours": popular_tours_data,
                    "prev_page": has_prev,
                    "next_page": has_next}), 200


@tours_bp.route("/categories/<string:category_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все туры для этой категории постранично'
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
        },
        {
            'name': 'page',
            'type': 'integer',
            'required': False,
            'description': 'Номер страницы для пагинации (по умолчанию 1)',
            'in': 'query'
        }
    ]
})
def show_category_page(category_id: str):
    """
           Возвращает все туры, относящиеся к данной категории постранично
           ---
           """

    try:
        valid_category_uuid = UUID(category_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()

        if not category:
            return jsonify({"success": False,
                "message": "Категория не найдена"}), 404

        page = request.args.get('page', 1, type=int)
        tours_for_category = category.tours.paginate(
        page=page, per_page=int(os.getenv("TOURS_PER_PAGE")), error_out=False)
        tours_schema = TourSchema(many=True, exclude=("tour_text",))
        tours_for_category_data = tours_schema.dump(tours_for_category)

        return jsonify({"success": True,
                        "tours": tours_for_category_data,
                        "prev_page": tours_for_category.has_prev,
                        "next_page": tours_for_category.has_next}), 200

    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории'}), 400


@tours_bp.route("/<string:tour_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этому туру, комментарии - постранично'
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
            'name': 'page',
            'type': 'integer',
            'required': False,
            'description': 'Номер страницы для пагинации (по умолчанию 1)',
            'in': 'query'
        }
    ]
})
@jwt_required()
def show_tour_page(tour_id: str):
    """
       Возвращает всю информацию про конкретный тур, комментарии - постранично
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

    page = request.args.get('page', 1, type=int)
    tour_schema = TourSchema()
    replies_schema = ReplySchema(many=True)
    tour_data = tour_schema.dump(tour)
    replies= tour.tour_replies.paginate(
        page=page, per_page=int(os.getenv("REPLIES_PER_PAGE")), error_out=False)

    return jsonify({"success": True,
                    "tour": tour_data,
                    "tour_replies": replies_schema.dump(replies),
                    "prev_page": replies.has_prev,
                    "next_page": replies.has_next}), 200


@tours_bp.route("/countries/<string:country_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все туры для этой страны постранично'
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
        },
        {
            'name': 'page',
            'type': 'integer',
            'required': False,
            'description': 'Номер страницы для пагинации (по умолчанию 1)',
            'in': 'query'
        }
    ]
})
def show_country_page(country_id: str):
    """
        Возвращает все туры, относящиеся к данной стране постранично
       ---
       """

    try:
        valid_country_uuid = UUID(country_id)
        country = Country.query.filter_by(country_id=valid_country_uuid).first()

        if not country:
            return jsonify({"success": False,
                    "message": "Страна не найдена"}), 404

        page = request.args.get('page', 1, type=int)
        tours_for_country = country.tours.paginate(
        page=page, per_page=int(os.getenv("TOURS_PER_PAGE")), error_out=False)
        tours_schema = TourSchema(many=True, exclude=("tour_text",))
        tours_for_country_data = tours_schema.dump(tours_for_country)

        return jsonify({"success": True,
                        "tours": tours_for_country_data,
                        "prev_page": tours_for_country.has_prev,
                        "next_page": tours_for_country.has_next}), 200

    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у страны'}), 400


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

    tour_schema = TourSchema(exclude=("tour_text", "tour_image"))
    tour_data = tour_schema.dump(tour)

    return jsonify({"success": True,
                    "tour": tour_data}), 200


@tours_bp.route('/<string:tour_id>/payment', methods=['POST'])
@swag_from({
    'consumes': ['application/json'],
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
    'consumes': ['application/json'],
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


@tours_bp.route('/<string:tour_id>/add_reply', methods=['POST'])
@swag_from({
    'consumes': ['application/json'],
    'responses': {
        201: {
            'description': 'Добавил комментарий'
        },
        400: {
            'description': 'Данные комментария не прошли проверку или неверный формат uuid'
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
            'name': 'reply',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'reply_text': {
                        'type': 'string',
                        'description': 'Текст комментария, обязательно для заполнения'
                    },
                    'parent_reply_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'ID родительского комментария, необязательно для заполнения - '
                                       'если комментарий корневой'
                    }
                },
                'required': ['reply_text']
            }
        }
    ]
})
@jwt_required()
def add_reply(tour_id: str):
    """
        Оставляет комментарий
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
    reply_schema = ReplySchema(unknown=EXCLUDE)

    try:
        reply = reply_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"success": False,
                        "errors": err.messages}), 400

    if reply.parent_reply_id:
        parent_reply = Reply.query.filter_by(reply_id=json_data.get("parent_reply_id")).first()
        if not parent_reply:
            return jsonify({"success": False,
                            "message": "Родительский комментарий не найден"}), 404
        else:
            if current_user.role != "moderator":
                return jsonify({"success": False,
                                "message": "Только модераторы могут отвечать на чужие вопросы"}), 401
            if parent_reply.replies:
                return jsonify({"success": False,
                                "message": "На данный комментарий уже дан ответ"}), 400

    db.session.add(reply)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Комментарий успешно сохранён!",
                    "reply": reply_schema.dump(reply)}), 201


@tours_bp.route("/replies/<string:reply_id>/delete", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Комментарий успешно удалён'
        },
        400: {
            'description': 'Неверный формат UUID комментария'
        },
        401: {
            'description': 'JWT токен с данными пользователя не прошел проверку или у него недостаточно прав'
        },
        404: {
            'description': 'Если комментария с таким ID нет'
        }
    },
    'parameters': [
        {
            'name': 'reply_id',
            'description': 'ID комментария',
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
def delete_reply(reply_id: str):
    """
       Удаляет выбранный комментарий
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'moderator':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    try:
        valid_reply_uuid = UUID(reply_id)
    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у комментария'}), 400

    reply = Reply.query.filter_by(reply_id=valid_reply_uuid).first()

    if not reply:
        return jsonify({"success": False,
            "message": "Комментарий с таким ID не найден"}), 404

    db.session.delete(reply)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Комментарий успешно удалён!"}), 200
