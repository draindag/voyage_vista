from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, abort
from sqlalchemy import func

from webapp import db
from webapp.models.Category import Category
from webapp.models.Review import Review
from webapp.models.Tour import Tour
from webapp.models.Country import Country

tours_bp = Blueprint("tours", __name__)


@tours_bp.route("/api/tours/categories", methods=["GET"])
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
    categories_data = [category.to_dict() for category in categories]
    return jsonify(categories_data)


@tours_bp.route("/api/tours/special_offers", methods=["GET"])
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
    discounts_tours_data = []
    for tour in tours_with_discounts:
        tour_data = tour.to_dict()
        tour_data['category'] = tour.category.to_dict()
        tour_data['country'] = tour.country.to_dict()
        discounts_tours_data.append(tour_data)
    return jsonify(discounts_tours_data)


@tours_bp.route("/api/tours/popular", methods=["GET"])
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
        func.avg(Review.review_value).desc()).limit(30).all()
    popular_tours_data = []
    for tour in popular_tours:
        tour_data = tour.to_dict()
        tour_data['category'] = tour.category.to_dict()
        tour_data['country'] = tour.country.to_dict()
        tour_data['rating'] = tour.get_rating()
        popular_tours_data.append(tour_data)
    return jsonify(popular_tours_data)


@tours_bp.route("/api/tours/categories/<string:category_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все туры для этой категории'
        },
        404: {
            'description': 'Если категории с таким id нет или неверный формат uuid'
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
        category = Category.query.filter_by(category_id=valid_category_uuid).first_or_404()
        tours_for_category = Tour.query.filter_by(category_id=category_id).all()
        tours_for_category_data = []
        for tour in tours_for_category:
            tour_data = tour.to_dict()
            tour_data['category'] = tour.category.to_dict()
            tour_data['country'] = tour.country.to_dict()
            tours_for_category_data.append(tour_data)
        return jsonify(tours_for_category_data)
    except ValueError:
        abort(404)


@tours_bp.route("/api/tours/categories/<string:category_id>/<string:tour_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этому туру'
        },
        404: {
            'description': 'Если категории или тура с таким id нет или неверный формат uuid'
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
def show_tour_page(category_id: str, tour_id: str):
    """
       Возвращает всю информацию про конкретный тур
       ---
       """

    try:
        valid_category_uuid = UUID(category_id)
        valid_tour_uuid = UUID(tour_id)
        category = Category.query.filter_by(category_id=valid_category_uuid).first_or_404()
        tour = Tour.query.filter_by(tour_id=valid_tour_uuid, category_id=valid_category_uuid).first_or_404()
        tour_data = tour.to_dict()
        tour_data['category'] = tour.category.to_dict()
        tour_data['country'] = tour.country.to_dict()
        return jsonify(tour_data)
    except ValueError:
        abort(404)


@tours_bp.route("/api/tours/countries/<string:country_id>", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул информацию по этой стране'
        },
        404: {
            'description': 'Если страны с таким id нет или неверный формат uuid'
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
        country = Country.query.filter_by(country_id=country_id).first_or_404()
        return jsonify(country.to_dict())
    except ValueError:
        abort(404)
