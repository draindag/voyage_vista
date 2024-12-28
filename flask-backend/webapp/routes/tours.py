"""
Этот модуль определяет маршруты API, связанные с ключевыми объектами
веб-сайта - турами, категориями, странами и так далее
"""

import os
from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy import func

from webapp import db
from webapp.bot import send_notification
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
@swag_from("swagger_definitions/show_categories.yaml")
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
@swag_from("swagger_definitions/show_tours_with_discounts.yaml")
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
@swag_from("swagger_definitions/show_most_popular_tours.yaml")
def show_most_popular_tours():
    """
       Возвращает первые 20 туров с самой высокой оценкой
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
@swag_from("swagger_definitions/show_category_page.yaml")
def show_category_page(category_id: str):
    """
           Возвращает все туры, относящиеся к данной категории постранично
           ---
           """

    try:
        valid_category_uuid = UUID(category_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first()
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у категории'}), 400

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


@tours_bp.route("/<string:tour_id>", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_tour_page.yaml")
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
@swag_from("swagger_definitions/show_country_page.yaml")
def show_country_page(country_id: str):
    """
        Возвращает все туры, относящиеся к данной стране постранично
       ---
       """

    try:
        valid_country_uuid = UUID(country_id)
        country = Country.query.filter_by(country_id=valid_country_uuid).first()
    except ValueError:
        return jsonify({"success": False,
                        'error': 'Неверный формат ID у страны'}), 400

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
                    "country_image": country.country_image,
                    "prev_page": tours_for_country.has_prev,
                    "next_page": tours_for_country.has_next}), 200


@tours_bp.route('/<string:tour_id>/to_favourite', methods=['POST'])
@jwt_required()
@swag_from("swagger_definitions/add_tour_to_favourites.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/unfavourite_tour.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/show_tour_payment_info.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/add_transaction.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/add_review_to_tour.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/add_reply.yaml")
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
    else:
        send_notification(current_user.login, tour.category.category_title, tour.tour_title, reply.reply_text)

    db.session.add(reply)
    db.session.commit()

    return jsonify({"success": True,
                    "message": "Комментарий успешно сохранён!",
                    "reply": reply_schema.dump(reply)}), 201


@tours_bp.route("/replies/<string:reply_id>/delete", methods=["DELETE"])
@jwt_required()
@swag_from("swagger_definitions/delete_reply.yaml")
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