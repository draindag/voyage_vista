from flasgger import swag_from
from flask import Blueprint, jsonify

from webapp.models.Category import Category
from webapp.schemas.CategorySchema import CategorySchema

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
       Возвращает все категории для туров
       ---
       """

    categories = Category.query.all()
    categories_schema = CategorySchema(many=True)
    categories_data = categories_schema.dump(categories)
    return jsonify(categories_data), 200
