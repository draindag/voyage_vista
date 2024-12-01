"""
Этот модуль определяет маршруты API, связанные с работой администратора:
добавление, изменение и удаление ключевых объектов веб-сайта
"""

import os
from uuid import UUID

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_uploads import UploadNotAllowed
from marshmallow import ValidationError, EXCLUDE

from webapp import db, photos
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

upload_folder = os.getenv("UPLOADED_PHOTOS_DEST")
file_ext = os.getenv("COVER_IMAGES_EXT")

@admin_bp.route("/categories", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_categories_for_admin.yaml")
def show_categories_for_admin():
    """
       Возвращает все категории для панели админа постранично
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                "message": "Неизвестный пользователь!"}), 401

    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(
        page=page, per_page=int(os.getenv("CATEGORIES_PER_PAGE_ADMIN_PANEL")), error_out=False)
    categories_schema = CategorySchema(many=True, exclude=("category_image",))
    categories_data = categories_schema.dump(categories)

    return jsonify({"success": True,
                     "categories": categories_data,
                    "prev_page": categories.has_prev,
                    "next_page": categories.has_next}), 200


@admin_bp.route("/countries", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_countries_for_admin.yaml")
def show_countries_for_admin():
    """
       Возвращает все страны для панели админа постранично
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    page = request.args.get('page', 1, type=int)
    countries = Country.query.paginate(
        page=page, per_page=int(os.getenv("COUNTRIES_PER_PAGE_ADMIN_PANEL")), error_out=False)
    countries_schema = CountrySchema(many=True, exclude=("country_image",))
    countries_data = countries_schema.dump(countries)
    return jsonify({"success": True,
                    "countries": countries_data,
                    "prev_page": countries.has_prev,
                    "next_page": countries.has_next}), 200


@admin_bp.route("/tours", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_tours_for_admin.yaml")
def show_tours_for_admin():
    """
       Возвращает все туры для панели админа постранично
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    page = request.args.get('page', 1, type=int)
    tours = Tour.query.paginate(
        page=page, per_page=int(os.getenv("TOURS_PER_PAGE_ADMIN_PANEL")), error_out=False)
    tours_schema = TourSchema(many=True,  exclude=("tour_text", "tour_description", "tour_price",
                                                   "tour_start_date", "tour_end_date", "offers", "price_with_discount",
                                                   "tour_image"))
    tours_data = tours_schema.dump(tours)
    return jsonify({"success": True,
                    "tours": tours_data,
                    "prev_page": tours.has_prev,
                    "next_page": tours.has_next}), 200


@admin_bp.route("/offers", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_offers_for_admin.yaml")
def show_offers_for_admin():
    """
       Возвращает все акции для панели админа постранично
       ---
       """

    user_login = get_jwt_identity()
    current_user = User.query.filter_by(login=user_login).first()

    if current_user is None or current_user.role != 'admin':
        return jsonify({"success": False,
                        "message": "Неизвестный пользователь!"}), 401

    page = request.args.get('page', 1, type=int)
    offers = SpecialOffer.query.paginate(
        page=page, per_page=int(os.getenv("OFFERS_PER_PAGE_ADMIN_PANEL")), error_out=False)
    offers_schema = OfferSchema(many=True)
    offers_data = offers_schema.dump(offers)
    return jsonify({"success": True,
                    "special_offers": offers_data,
                    "prev_page": offers.has_prev,
                    "next_page": offers.has_next}), 200


@admin_bp.route("/categories/new", methods=["POST"])
@jwt_required()
@swag_from("swagger_definitions/add_category.yaml")
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

    category_data = {
        "category_title": request.form.get("category_title"),
        "category_description": request.form.get("category_description"),
    }

    category_exists = Category.query.filter_by(category_title=category_data.get("category_title")).first()
    if category_exists:
        return {"success": False,
                "message": "Категория с таким названием уже существует"}, 400

    category_schema = CategorySchema(unknown=EXCLUDE)

    try:
        category = category_schema.load(category_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    if not 'cover_image' in request.files:
        return jsonify({'error': 'Обложка категории обязательна!'}), 400

    cover_image = request.files['cover_image']

    if cover_image.filename == '':
        return jsonify({'error': 'Выбранного файла не существует'}), 400

    db.session.add(category)

    temp_filename = f"temp{file_ext}"
    try:
        photos.save(cover_image, name=temp_filename)
    except UploadNotAllowed:
        db.session.rollback()
        return jsonify({"success": False,
                        'error': "Файл не является изображением"}), 400

    db.session.commit()

    existing_filename = os.path.join(upload_folder, temp_filename)
    final_filename = f"{str(category.category_id)}{file_ext}"
    new_filepath = os.path.join(upload_folder, final_filename)
    os.rename(existing_filename, new_filepath)

    return jsonify({
        "success": True,
        "message": "Категория успешно добавлена!",
        "category": category_schema.dump(category)
    }), 201



@admin_bp.route("/categories/<string:category_id>/edit", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_category_edit_page.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/edit_category.yaml")
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

    category_data = {
        "category_title": request.form.get("category_title"),
        "category_description": request.form.get("category_description"),
    }

    category = Category.query.filter_by(category_id=valid_category_uuid).first()

    if not category:
        return jsonify({"success": False,
            "message": "Категория с таким ID не найдена"}), 404

    if category.category_title != category_data.get("category_title"):
        category_exists = Category.query.filter_by(category_title=category_data.get("category_title")).first()
        if category_exists:
            return jsonify({"success": False,
                    "message": "Категория с таким названием уже существует"}), 400

    category_schema = CategorySchema(unknown=EXCLUDE)

    try:
        update_data = category_schema.load(category_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    cover_image = None
    if 'cover_image' in request.files:
        cover_image = request.files['cover_image']

    if cover_image and cover_image.filename == '':
        return jsonify({'error': 'Выбранного файла не существует'}), 400

    for key, value in category_data.items():
        setattr(category, key, value)

    if cover_image:
        temp_filename = f"temp{file_ext}"
        try:
            photos.save(cover_image, name=temp_filename)
        except UploadNotAllowed:
            db.session.rollback()
            return jsonify({"success": False,
                            'error': "Файл не является изображением"}), 400

        old_file = f"{str(category.category_id)}{file_ext}"
        old_file_path = os.path.join(upload_folder, old_file)
        if os.path.isfile(old_file_path):
            os.remove(old_file_path)

        existing_filename = os.path.join(upload_folder, temp_filename)
        final_filename = f"{str(category.category_id)}{file_ext}"
        new_filepath = os.path.join(upload_folder, final_filename)
        os.rename(existing_filename, new_filepath)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные категории успешно изменены!",
        "category": category_schema.dump(category)
    }), 200


@admin_bp.route("/categories/<string:category_id>/delete", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_category_delete_page.yaml")
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

        category_schema = CategorySchema(exclude=("category_image",))

        category_data = category_schema.dump(category)

        return jsonify({"success": True,
            "category": category_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у категории'}), 400


@admin_bp.route("/categories/<string:category_id>/delete", methods=["DELETE"])
@jwt_required()
@swag_from("swagger_definitions/delete_category.yaml")
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

    cover_image = f"{str(category.category_id)}{file_ext}"
    cover_image_path = os.path.join(upload_folder, cover_image)
    if os.path.isfile(cover_image_path):
        os.remove(cover_image_path)

    return jsonify({"success": True,
                    "message": "Категория успешно удалена!"}), 200


@admin_bp.route("/countries/new", methods=["POST"])
@jwt_required()
@swag_from("swagger_definitions/add_country.yaml")
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

    country_data = {
        "country_name": request.form.get("country_name"),
        "country_description": request.form.get("country_description"),
    }

    country_exists = Country.query.filter_by(country_name=country_data.get("country_name")).first()
    if country_exists:
        return jsonify({"success": False,
                "message": "Страна с таким названием уже существует"}), 400

    country_schema = CountrySchema(unknown=EXCLUDE)

    try:
        country = country_schema.load(country_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    if not 'cover_image' in request.files:
        return jsonify({'error': 'Обложка страны обязательна!'}), 400

    cover_image = request.files['cover_image']

    if cover_image.filename == '':
        return jsonify({'error': 'Выбранного файла не существует'}), 400

    db.session.add(country)

    temp_filename = f"temp{file_ext}"
    try:
        photos.save(cover_image, name=temp_filename)
    except UploadNotAllowed:
        db.session.rollback()
        return jsonify({"success": False,
                        'error': "Файл не является изображением"}), 400
    db.session.commit()

    existing_filename = os.path.join(upload_folder, temp_filename)
    final_filename = f"{str(country.country_id)}{file_ext}"
    new_filepath = os.path.join(upload_folder, final_filename)
    os.rename(existing_filename, new_filepath)

    return jsonify({
        "success": True,
        "message": "Страна успешно добавлена!",
        "country": country_schema.dump(country)
    }), 201


@admin_bp.route("/countries/<string:country_id>/edit", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_country_edit_page.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/edit_country.yaml")
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

    country_data = {
        "country_name": request.form.get("country_name"),
        "country_description": request.form.get("country_description"),
    }

    country = Country.query.filter_by(country_id=valid_country_uuid).first()

    if not country:
        return jsonify({"success": False,
            "message": "Страна с таким ID не найдена"}), 404

    if country.country_name != country_data.get("country_name"):
        country_exists = Country.query.filter_by(country_name=country_data.get("country_name")).first()
        if country_exists:
            return jsonify({"success": False,
                    "message": "Страна с таким названием уже существует"}), 400

    country_schema = CountrySchema(unknown=EXCLUDE)

    try:
        update_data = country_schema.load(country_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    cover_image = None
    if 'cover_image' in request.files:
        cover_image = request.files['cover_image']

    if cover_image and cover_image.filename == '':
        return jsonify({'error': 'Выбранного файла не существует'}), 400

    for key, value in country_data.items():
        setattr(country, key, value)

    if cover_image:
        temp_filename = f"temp{file_ext}"
        try:
            photos.save(cover_image, name=temp_filename)
        except UploadNotAllowed:
            db.session.rollback()
            return jsonify({"success": False,
                            'error': "Файл не является изображением"}), 400

        old_file = f"{str(country.country_id)}{file_ext}"
        old_file_path = os.path.join(upload_folder, old_file)
        if os.path.isfile(old_file_path):
            os.remove(old_file_path)

        existing_filename = os.path.join(upload_folder, temp_filename)
        final_filename = f"{str(country.country_id)}{file_ext}"
        new_filepath = os.path.join(upload_folder, final_filename)
        os.rename(existing_filename, new_filepath)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные страны успешно изменены!",
        "category": country_schema.dump(country)
    }), 200


@admin_bp.route("/countries/<string:country_id>/delete", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_country_delete_page.yaml")
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

        country_schema = Country(exclude=("country_image",))

        country_data = country_schema.dump(country)

        return jsonify({"success": True,
            "country": country_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у страны'}), 400


@admin_bp.route("/countries/<string:country_id>/delete", methods=["DELETE"])
@jwt_required()
@swag_from("swagger_definitions/delete_country.yaml")
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

    cover_image = f"{str(country.country_id)}{file_ext}"
    cover_image_path = os.path.join(upload_folder, cover_image)
    if os.path.isfile(cover_image_path):
        os.remove(cover_image_path)

    return jsonify({"success": True,
                    "message": "Страна успешно удалена!"}), 200


@admin_bp.route("/tours/new", methods=["POST"])
@jwt_required()
@swag_from("swagger_definitions/add_tour.yaml")
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

    tour_data = {
        "tour_title": request.form.get("tour_title"),
        "tour_description": request.form.get("tour_description"),
        "tour_text": request.form.get("tour_text"),
        "tour_price": request.form.get("tour_price"),
        "tour_start_date": request.form.get("tour_start_date"),
        "tour_end_date": request.form.get("tour_end_date"),
        "category_id": request.form.get("category_id"),
        "country_id": request.form.get("country_id"),
        "offer_id": request.form.get("offer_id")
    }


    tour_title = tour_data.get("tour_title")
    category_id = tour_data.get("category_id")
    country_id = tour_data.get("country_id")
    offer_id = tour_data.get("offer_id")

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

    tour_schema = TourSchema(unknown=EXCLUDE)

    try:
        tour = tour_schema.load(tour_data)
    except ValidationError as err:
        return jsonify({"success": False,
                "errors": err.messages}), 400

    tour_exists_in_that_category = Tour.query.filter_by(tour_title=tour_title, category_id=category_id).first()
    if tour_exists_in_that_category:
        return jsonify({"success": False,
                "message": "Тур с таким названием уже существует в этой категории"}), 400

    if not 'cover_image' in request.files:
        return jsonify({'error': 'Обложка тура обязательна!'}), 400

    cover_image = request.files['cover_image']

    if cover_image.filename == '':
        return jsonify({'error': 'Выбранного файла не существует'}), 400

    db.session.add(tour)
    if offer:
        tour.offers.append(offer)

    temp_filename = f"temp{file_ext}"
    try:
        photos.save(cover_image, name=temp_filename)
    except UploadNotAllowed:
        db.session.rollback()
        return jsonify({"success": False,
                        'error': "Файл не является изображением"}), 400
    db.session.commit()

    existing_filename = os.path.join(upload_folder, temp_filename)
    final_filename = f"{str(tour.tour_id)}{file_ext}"
    new_filepath = os.path.join(upload_folder, final_filename)
    os.rename(existing_filename, new_filepath)

    return jsonify({
        "success": True,
        "message": "Тур успешно добавлен!",
        "tour": tour_schema.dump(tour)
    }), 201


@admin_bp.route("/tours/<string:tour_id>/edit", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_tour_edit_page.yaml")
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

        tour_schema = TourSchema()

        tour_data = tour_schema.dump(tour)

        return jsonify({"success": True,
            "tour": tour_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400


@admin_bp.route("/tours/<string:tour_id>/edit", methods=["PUT"])
@jwt_required()
@swag_from("swagger_definitions/edit_tour.yaml")
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

    tour_data = {
        "tour_title": request.form.get("tour_title"),
        "tour_description": request.form.get("tour_description"),
        "tour_text": request.form.get("tour_text"),
        "tour_price": request.form.get("tour_price"),
        "tour_start_date": request.form.get("tour_start_date"),
        "tour_end_date": request.form.get("tour_end_date"),
        "category_id": request.form.get("category_id"),
        "country_id": request.form.get("country_id"),
        "offer_id": request.form.get("offer_id")
    }

    tour_title = tour_data.get("tour_title")
    category_id = tour_data.get("category_id")
    country_id = tour_data.get("country_id")
    offer_id = tour_data.get("offer_id")

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
            "message": "Тур с таким ID не найден"}), 404

    tour_schema = TourSchema(unknown=EXCLUDE)

    try:
        update_data = tour_schema.load(tour_data)
    except ValidationError as err:
        return jsonify({"success": False,
            "errors": err.messages}), 400

    if tour.tour_title != tour_title:
        tour_exists = Tour.query.filter_by(tour_title=tour_title, category_id=category_id).first()
        if tour_exists:
            return jsonify({"success": False,
                    "message": "Тур с таким названием уже существует в этой категории"}), 400

    cover_image = None
    if 'cover_image' in request.files:
        cover_image = request.files['cover_image']

    if cover_image and cover_image.filename == '':
        return jsonify({'error': 'Выбранного файла не существует'}), 400

    for key, value in tour_data.items():
        setattr(tour, key, value)

    if tour.offers.first() != offer:
        for special_offer in tour.offers.all():
            tour.offers.remove(special_offer)
        if offer_id:
            tour.offers.append(offer)

    if cover_image:
        temp_filename = f"temp{file_ext}"
        try:
            photos.save(cover_image, name=temp_filename)
        except UploadNotAllowed:
            db.session.rollback()
            return jsonify({"success": False,
                            'error': "Файл не является изображением"}), 400

        old_file = f"{str(tour.tour_id)}{file_ext}"
        old_file_path = os.path.join(upload_folder, old_file)
        if os.path.isfile(old_file_path):
            os.remove(old_file_path)

        existing_filename = os.path.join(upload_folder, temp_filename)
        final_filename = f"{str(tour.tour_id)}{file_ext}"
        new_filepath = os.path.join(upload_folder, final_filename)
        os.rename(existing_filename, new_filepath)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Данные тура успешно изменены!",
        "tour": tour_schema.dump(tour)
    }), 200


@admin_bp.route("/tours/<string:tour_id>/delete", methods=["GET"])
@jwt_required()
@swag_from("swagger_definitions/show_tour_delete_page.yaml")
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

        tour_schema = TourSchema(exclude=("tour_text", "offers", "tour_image"))

        tour_data = tour_schema.dump(tour)

        return jsonify({"success": True,
            "tour": tour_data}), 200

    except ValueError:
        return jsonify({"success": False,
            'error': 'Неверный формат ID у тура'}), 400


@admin_bp.route("/tours/<string:tour_id>/delete", methods=["DELETE"])
@jwt_required()
@swag_from("swagger_definitions/delete_tour.yaml")
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

    cover_image = f"{str(tour.tour_id)}{file_ext}"
    cover_image_path = os.path.join(upload_folder, cover_image)
    if os.path.isfile(cover_image_path):
        os.remove(cover_image_path)

    return jsonify({"success": True,
                    "message": "Тур успешно удалён!"}), 200


@admin_bp.route("/offers/new", methods=["POST"])
@jwt_required()
@swag_from("swagger_definitions/add_special_offer.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/show_special_offer_edit_page.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/edit_special_offer.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/show_special_offer_delete_page.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/delete_special_offer.yaml")
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
@jwt_required()
@swag_from("swagger_definitions/registrate_moderator.yaml")
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
