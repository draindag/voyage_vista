from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route("/api", methods=["GET"])
def index():
    """
       Это описание для Swagger.
       ---
       responses:
         200:
           description: пробный метод
       """

    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    return jsonify(data)
