"""
Этот модуль определяет основной маршрут API для извлечения категорий туров
и стран.

Он возвращает данные для слайдера категорий и выпадающего списка стран
на главной странице приложения.
"""

from flasgger import swag_from
from flask import Blueprint, jsonify

from webapp.models.Category import Category
from webapp.models.Country import Country
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema

main_bp = Blueprint('main', __name__)


@main_bp.route("/categories_all", methods=["GET"])
@swag_from("swagger_definitions/index_categories.yaml")
def index_categories():
    """
       Возвращает все категории туров для слайдера на главной
       ---
       """

    categories = Category.query.all()
    categories_schema = CategorySchema(many=True)
    categories_data = categories_schema.dump(categories)

    return jsonify({"success": True,
                    "categories": categories_data}), 200


@main_bp.route("/countries_all", methods=["GET"])
@swag_from("swagger_definitions/index_countries.yaml")
def index_countries():
    """
       Возвращает все страны для выпадающего списка на главной
       ---
       """

    countries = Country.query.all()
    country_schema = CountrySchema(many=True, exclude=("country_image",))
    countries_data = country_schema.dump(countries)

    return jsonify({"success": True,
                    "countries": countries_data}), 200
