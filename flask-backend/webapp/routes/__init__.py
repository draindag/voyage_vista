from flasgger import swag_from
from flask import Blueprint, jsonify

from webapp.models.Category import Category
from webapp.models.Country import Country
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema

main_bp = Blueprint('main', __name__)


@main_bp.route("/api", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Вернул все категории'
        }
    }
})
def index():
    """
       Возвращает все категории туров для слайдера и страны для выпадающего списка на главной
       ---
       """

    categories = Category.query.all()
    categories_schema = CategorySchema(many=True)
    categories_data = categories_schema.dump(categories)

    countries = Country.query.all()
    country_schema = CountrySchema(many=True)
    countries_data = country_schema.dump(countries)

    return jsonify({"success": True,
                    "categories": categories_data,
                    "countries": countries_data}), 200
