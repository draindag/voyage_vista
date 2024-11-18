from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify
from sqlalchemy import func

from webapp import db
from webapp.models.Category import Category
from webapp.models.Review import Review
from webapp.models.Tour import Tour
from webapp.models.Country import Country
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema
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
        404: {
            'description': 'Если категории или тура с таким id нет'
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
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
def show_tour_page_from_category(category_id: str, tour_id: str):
    """
       Возвращает всю информацию про конкретный тур
       ---
       """

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
        404: {
            'description': 'Если страны или тура с таким id нет'
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
            'name': 'tour_id',
            'description': 'ID тура',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
def show_tour_page_from_country(country_id: str, tour_id: str):
    """
       Возвращает всю информацию про конкретный тур
       ---
       """

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
