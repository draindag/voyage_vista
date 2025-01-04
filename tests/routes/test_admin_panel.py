from io import BytesIO
import uuid

from webapp import db
from webapp.models.SpecialOffer import SpecialOffer
from webapp.models.Category import Category
from webapp.models.Country import Country


def test_show_categories_for_admin(auth_admin, category, db_session):
    """
    Тестирует успешное получение категорий для администратора
    """
    response = auth_admin.get('api/admin_panel/categories?page=1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'categories' in data
    assert len(data['categories']) > 0
    assert 'prev_page' in data
    assert 'next_page' in data

def test_show_categories_for_non_admin(auth_moderator, category, db_session):
    """
    Проверка, что модератор не может получить доступ к категориям админа
    """
    response = auth_moderator.get('api/admin_panel/categories?page=1')

    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == "Неизвестный пользователь!"

def test_show_countries_for_admin(auth_admin, country, db_session):
    """
    Тестирует успешное получение стран для администратора
    """
    response = auth_admin.get('api/admin_panel/countries?page=1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'countries' in data
    assert len(data['countries']) > 0
    assert 'prev_page' in data
    assert 'next_page' in data

def test_show_countries_for_non_admin(auth_moderator, country, db_session):
    """
    Проверка, что модератор не может получить доступ к категориям админа
    """
    response = auth_moderator.get('api/admin_panel/countries?page=1')

    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == "Неизвестный пользователь!"

def test_show_tours_for_admin(auth_admin, tour, db_session):
    """
    Тестирует успешное получение туров для администратора
    """
    response = auth_admin.get('api/admin_panel/tours?page=1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'tours' in data
    assert len(data['tours']) > 0
    assert 'prev_page' in data
    assert 'next_page' in data

def test_show_tours_for_non_admin(auth_moderator, tour, db_session):
    """
    Проверка, что модератор не может получить доступ к турам админа
    """
    response = auth_moderator.get('api/admin_panel/tours?page=1')

    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == "Неизвестный пользователь!"


def test_show_offers_for_admin(auth_admin, offer, db_session):
    """
    Тестирует успешное получение акций для администратора
    """
    response = auth_admin.get('api/admin_panel/offers?page=1')

    assert response.status_code == 200
    data = response.get_json()

    assert data['success'] is True
    assert 'special_offers' in data
    assert len(data['special_offers']) > 0
    assert 'prev_page' in data
    assert 'next_page' in data


def test_show_offers_for_non_admin(auth_moderator, offer, db_session):
    """
    Проверка, что модератор не может получить доступ к акциям админа
    """
    response = auth_moderator.get('api/admin_panel/offers?page=1')

    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == "Неизвестный пользователь!"


def test_show_offers_all(auth_admin, offer, db_session):
    """
    Тестирует успешное получение всех акций
    """
    response = auth_admin.get('api/admin_panel/offers_all')

    assert response.status_code == 200
    data = response.get_json()

    assert data['success'] is True
    assert 'special_offers' in data
    assert len(data['special_offers']) > 0
    assert isinstance(data['special_offers'], list)


def test_show_offers_all_empty(auth_admin, db_session):
    """
    Проверка, что возвращается пустой список, если нет акций
    """
    SpecialOffer.query.delete()
    db_session.commit()

    response = auth_admin.get('api/admin_panel/offers_all')

    assert response.status_code == 200
    data = response.get_json()

    assert data['success'] is True
    assert 'special_offers' in data
    assert len(data['special_offers']) == 0

def test_add_category_success(auth_admin, db_session):
    """
    Тестирует успешное добавление новой категории
    """
    category_data = {
        "category_title": "Adventure",
        "category_description": "Exciting and thrilling tours"
    }
    cover_image = (BytesIO(b"image content"), "cover_image.jpg")

    data = {
        "category_title": category_data["category_title"],
        "category_description": category_data["category_description"],
        "cover_image": cover_image
    }
    response = auth_admin.post('api/admin_panel/categories/new', data=data, content_type='multipart/form-data')

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Категория успешно добавлена!"
    assert "category" in data
    assert data["category"]["category_title"] == category_data["category_title"]

def test_add_category_missing_cover_image(auth_admin, db_session):
    """
    Проверка, что нельзя добавить категорию без обложки
    """
    category_data = {
        "category_title": "Adventure",
        "category_description": "Exciting and thrilling tours"
    }
    data = {
        "category_title": category_data["category_title"],
        "category_description": category_data["category_description"]
    }
    response = auth_admin.post('api/admin_panel/categories/new', data=data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Обложка категории обязательна!"

def test_add_category_invalid_cover_image(auth_admin, db_session):
    """
    Проверка, что нельзя загрузить файл, не являющийся изображением
    """
    category_data = {
        "category_title": "Adventure",
        "category_description": "Exciting and thrilling tours"
    }
    invalid_file = (BytesIO(b"not an image"), "cover_image.txt")
    data = {
        "category_title": category_data["category_title"],
        "category_description": category_data["category_description"],
        "cover_image": invalid_file
    }
    response = auth_admin.post('api/admin_panel/categories/new', data=data, content_type='multipart/form-data')

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Файл не является изображением"

def test_add_category_forbidden_for_non_admin(auth_moderator, db_session):
    """
    Проверка, что модератор не может добавить категорию
    """
    category_data = {
        "category_title": "Adventure",
        "category_description": "Exciting and thrilling tours"
    }
    cover_image = (BytesIO(b"image content"), "cover_image.jpg")

    data = {
        "category_title": category_data["category_title"],
        "category_description": category_data["category_description"],
        "cover_image": cover_image
    }
    response = auth_moderator.post('api/admin_panel/categories/new', data=data, content_type='multipart/form-data')

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неизвестный пользователь!"


def test_show_category_edit_page_success(auth_admin, category, db_session):
    """
    Тестирует успешное получение данных для редактирования категории
    """
    category_id = str(category.category_id)
    response = auth_admin.get(f'api/admin_panel/categories/{category_id}/edit')

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["category"]["category_title"] == category.category_title
    assert data["category"]["category_description"] == category.category_description


def test_show_category_edit_page_forbidden_for_non_admin(auth_moderator, category, db_session):
    """
    Проверка, что модератор не может получить данные для редактирования категории
    """
    category_id = str(category.category_id)
    response = auth_moderator.get(f'api/admin_panel/categories/{category_id}/edit')

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неизвестный пользователь!"


def test_show_category_edit_page_category_not_found(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка, если категория с таким ID не найдена
    """
    invalid_category_id = str(uuid.uuid4())

    response = auth_admin.get(f'api/admin_panel/categories/{invalid_category_id}/edit')

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Категория с таким ID не найдена"



def test_show_category_edit_page_invalid_category_id(auth_admin, db_session):
    """
    Проверка на неверный формат ID
    """
    invalid_category_id = "invalid_uuid"
    response = auth_admin.get(f'api/admin_panel/categories/{invalid_category_id}/edit')

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у категории"


def test_edit_category_success(auth_admin, category, db_session):
    """
    Тестирует успешное редактирование категории
    """
    category_id = str(category.category_id)
    new_category_data = {
        "category_title": "New Adventure",
        "category_description": "Updated description for exciting tours"
    }

    data = {
        "category_title": new_category_data["category_title"],
        "category_description": new_category_data["category_description"]
    }

    response = auth_admin.put(f'api/admin_panel/categories/{category_id}/edit', data=data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Данные категории успешно изменены!"
    assert data["category"]["category_title"] == new_category_data["category_title"]
    assert data["category"]["category_description"] == new_category_data["category_description"]


def test_edit_category_name_already_exists(auth_admin, category, db_session):
    """
    Проверка, что нельзя изменить название категории на уже существующее
    """
    other_category = Category(category_title="New Adventure", category_description="Exciting and thrilling tours")
    db.session.add(other_category)
    db.session.commit()

    data = {
        "category_title": "New Adventure",
        "category_description": "Updated description"
    }

    response = auth_admin.put(f'api/admin_panel/categories/{category.category_id}/edit', data=data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Категория с таким названием уже существует"


def test_edit_category_invalid_category_id(auth_admin, db_session):
    """
    Проверка на неверный формат ID категории при редактировании
    """
    invalid_category_id = "invalid_uuid"
    data = {
        "category_title": "New Adventure",
        "category_description": "Updated description"
    }

    response = auth_admin.put(f'api/admin_panel/categories/{invalid_category_id}/edit', data=data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у категории"


def test_edit_category_without_cover_image(auth_admin, category, db_session):
    """
    Проверка успешного редактирования категории без изменения обложки
    """
    category_id = str(category.category_id)
    new_category_data = {
        "category_title": "New Adventure",
        "category_description": "Updated description for exciting tours"
    }

    data = {
        "category_title": new_category_data["category_title"],
        "category_description": new_category_data["category_description"]
    }

    response = auth_admin.put(f'api/admin_panel/categories/{category_id}/edit', data=data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Данные категории успешно изменены!"
    assert data["category"]["category_title"] == new_category_data["category_title"]


def test_edit_category_with_invalid_cover_image(auth_admin, category, db_session):
    """
    Проверка, что нельзя загрузить файл, не являющийся изображением
    """
    category_id = str(category.category_id)
    new_category_data = {
        "category_title": "New Adventure",
        "category_description": "Updated description for exciting tours"
    }
    invalid_file = (BytesIO(b"not an image"), "cover_image.txt")

    data = {
        "category_title": new_category_data["category_title"],
        "category_description": new_category_data["category_description"],
        "cover_image": invalid_file
    }

    response = auth_admin.put(f'api/admin_panel/categories/{category_id}/edit', data=data,
                              content_type='multipart/form-data')

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Файл не является изображением"

def test_show_category_delete_page_success(auth_admin, category, db_session):
    """
    Проверка успешного получения данных для страницы удаления категории
    """
    category_id = str(category.category_id)

    response = auth_admin.get(f'api/admin_panel/categories/{category_id}/delete')

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "category" in data
    assert data["category"]["category_id"] == str(category.category_id)


def test_show_category_delete_page_category_not_found(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка, если категория с таким ID не найдена
    """
    invalid_category_id = str(uuid.uuid4())

    response = auth_admin.get(f'api/admin_panel/categories/{invalid_category_id}/delete')

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Категория с таким ID не найдена"


def test_show_category_delete_page_invalid_category_id_format(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка при неверном формате ID категории
    """
    invalid_category_id = "invalid-uuid-format"

    response = auth_admin.get(f'api/admin_panel/categories/{invalid_category_id}/delete')

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у категории"


def test_delete_category_success(auth_admin, category, db_session):
    """
    Проверка успешного удаления категории
    """
    category_id = str(category.category_id)
    delete_data = {"acceptance": True}

    response = auth_admin.delete(f'api/admin_panel/categories/{category_id}/delete', json=delete_data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Категория успешно удалена!"

    deleted_category = Category.query.filter_by(category_id=category.category_id).first()
    assert deleted_category is None


def test_delete_category_category_not_found(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка, если категория с таким ID не найдена при удалении
    """
    invalid_category_id = str(uuid.uuid4())
    delete_data = {"acceptance": True}

    response = auth_admin.delete(f'api/admin_panel/categories/{invalid_category_id}/delete', json=delete_data)

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Категория с таким ID не найдена"


def test_delete_category_invalid_category_id_format(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка при неверном формате ID категории при удалении
    """
    invalid_category_id = "invalid-uuid-format"
    delete_data = {"acceptance": True}

    response = auth_admin.delete(f'api/admin_panel/categories/{invalid_category_id}/delete', json=delete_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у категории"


def test_delete_category_no_acceptance(auth_admin, category, db_session):
    """
    Проверка, что возвращается ошибка, если галочка согласия не установлена
    """
    category_id = str(category.category_id)
    delete_data = {"acceptance": False}

    response = auth_admin.delete(f'api/admin_panel/categories/{category_id}/delete', json=delete_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Если вы хотите удалить данную категорию, вам необходимо поставить галочку выше"

def test_add_country_success(auth_admin, db_session):
    """
    Тестирует успешное добавление страны
    """
    country_data = {
        "country_name": "Australia",
        "country_description": "The land down under"
    }

    cover_image = (BytesIO(b"image content"), "cover_image.jpg")
    files = {
        'country_name': country_data['country_name'],
        'country_description': country_data['country_description'],
        'cover_image': cover_image
    }

    response = auth_admin.post('/api/admin_panel/countries/new', data=files)

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Страна успешно добавлена!"
    assert data["country"]["country_name"] == country_data["country_name"]
    assert data["country"]["country_description"] == country_data["country_description"]


def test_add_country_exists(auth_admin, db_session):
    """
    Тестирует, что возвращается ошибка, если страна с таким названием уже существует
    """
    country_data = {
        "country_name": "Australia",
        "country_description": "The land down under"
    }

    cover_image = (BytesIO(b"image content"), "cover_image.jpg")
    files = {
        'country_name': country_data['country_name'],
        'country_description': country_data['country_description'],
        'cover_image': cover_image
    }

    response = auth_admin.post('/api/admin_panel/countries/new', data=files)
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True

    cover_image_content = BytesIO(b"image content")
    cover_image_content.name = "cover_image.jpg"

    files = {
        'country_name': country_data['country_name'],
        'country_description': country_data['country_description'],
        'cover_image': (cover_image_content, "cover_image.jpg")
    }

    response = auth_admin.post('/api/admin_panel/countries/new', data=files)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с таким названием уже существует"


def test_add_country_missing_cover_image(auth_admin, db_session):
    """
    Тестирует ошибку, если не указана обложка страны
    """
    country_data = {
        "country_name": "Australia",
        "country_description": "The land down under"
    }

    response = auth_admin.post('/api/admin_panel/countries/new', data=country_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Обложка страны обязательна!"


def test_add_country_invalid_image_format(auth_admin, db_session):
    """
    Тестирует ошибку, если выбранный файл не является изображением
    """
    country_data = {
        "country_name": "Australia",
        "country_description": "The land down under"
    }

    invalid_file = (BytesIO(b"not an image"), "cover_image.txt")
    files = {
        'country_name': country_data['country_name'],
        'country_description': country_data['country_description'],
        'cover_image': invalid_file
    }

    response = auth_admin.post('/api/admin_panel/countries/new', data=files)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Файл не является изображением"


def test_show_country_edit_page_success(auth_admin, country, db_session):
    """
    Тестирует успешное получение данных для страницы редактирования страны
    """
    country_id = str(country.country_id)

    response = auth_admin.get(f'/api/admin_panel/countries/{country_id}/edit')

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "country" in data
    assert data["country"]["country_id"] == str(country.country_id)


def test_show_country_edit_page_country_not_found(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка, если страна с таким ID не найдена
    """
    invalid_country_id = str(uuid.uuid4())

    response = auth_admin.get(f'/api/admin_panel/countries/{invalid_country_id}/edit')

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с таким ID не найдена"


def test_show_country_edit_page_invalid_country_id_format(auth_admin, db_session):
    """
    Проверка, что возвращается ошибка при неверном формате ID страны
    """
    invalid_country_id = "invalid-uuid-format"

    response = auth_admin.get(f'/api/admin_panel/countries/{invalid_country_id}/edit')

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у страны"

def test_edit_country_success(auth_admin, country, db_session):
    """
    Тестирует успешное редактирование страны
    """
    country_id = str(country.country_id)
    new_country_data = {
        "country_name": "New Zealand",
        "country_description": "The land of the long white cloud"
    }

    data = {
        "country_name": new_country_data["country_name"],
        "country_description": new_country_data["country_description"]
    }

    response = auth_admin.put(f'/api/admin_panel/countries/{country_id}/edit', data=data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Данные страны успешно изменены!"
    assert data["country"]["country_name"] == new_country_data["country_name"]
    assert data["country"]["country_description"] == new_country_data["country_description"]

def test_edit_country_name_exists(auth_admin, country, db_session):
    """
    Тестирует, что возвращается ошибка, если страна с таким названием уже существует
    """
    other_country = Country(country_name="New Country", country_description="Known for its beautiful mountains, lakes, and resorts.")
    db.session.add(other_country)
    db.session.commit()

    new_country_data = {
        "country_name": other_country.country_name,
        "country_description": "A new description"
    }

    response = auth_admin.put(f'/api/admin_panel/countries/{country.country_id}/edit', data=new_country_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с таким названием уже существует"

def test_edit_country_not_found(auth_admin, db_session):
    """
    Тестирует, что возвращается ошибка, если страна с таким ID не найдена
    """
    invalid_country_id = str(uuid.uuid4())
    new_country_data = {
        "country_name": "New Country",
        "country_description": "Description of the new country"
    }

    response = auth_admin.put(f'/api/admin_panel/countries/{invalid_country_id}/edit', data=new_country_data)

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с таким ID не найдена"

def test_edit_country_invalid_id_format(auth_admin, db_session):
    """
    Тестирует, что возвращается ошибка, если формат ID у страны неверный
    """
    invalid_country_id = "invalid_uuid"
    new_country_data = {
        "country_name": "New Country",
        "country_description": "Description of the new country"
    }

    response = auth_admin.put(f'/api/admin_panel/countries/{invalid_country_id}/edit', data=new_country_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у страны"

def test_edit_country_missing_data(auth_admin, country, db_session):
    """
    Тестирует, что возвращается ошибка, если отсутствуют обязательные данные
    """
    country_id = str(country.country_id)
    invalid_country_data = {
        "country_name": "",
        "country_description": "Description without a name"
    }

    response = auth_admin.put(f'/api/admin_panel/countries/{country_id}/edit', data=invalid_country_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "errors" in data
    assert "country_name" in data["errors"]

def test_show_country_delete_page_success(auth_admin, country):
    """
    Проверяет успешное получение данных страны для страницы удаления.
    """
    response = auth_admin.get(f"/api/admin_panel/countries/{country.country_id}/delete")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "country" in data
    assert data["country"]["country_name"] == country.country_name


def test_show_country_delete_page_not_found(auth_admin, db_session):
    """
    Проверяет, что возвращается ошибка, если страна с таким ID не найдена.
    """
    invalid_country_id = str(uuid.uuid4())
    response = auth_admin.get(f"/api/admin_panel/countries/{invalid_country_id}/delete")

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с таким ID не найдена"


def test_show_country_delete_page_invalid_uuid(auth_admin):
    """
    Проверяет, что возвращается ошибка при неверном формате ID.
    """
    invalid_format_id = "invalid-uuid"
    response = auth_admin.get(f"/api/admin_panel/countries/{invalid_format_id}/delete")

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у страны"


def test_show_country_delete_page_unauthorized(auth_moderator, country):
    """
    Проверяет, что неадминистраторский пользователь не имеет доступа.
    """
    response = auth_moderator.get(f"/api/admin_panel/countries/{country.country_id}/delete")

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неизвестный пользователь!"

def test_delete_country_success(auth_admin, country, db_session):
    """
    Тестирует успешное удаление существующей страны.
    """
    response = auth_admin.delete(
        f"/api/admin_panel/countries/{country.country_id}/delete",
        json={"acceptance": True},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Страна успешно удалена!"

    deleted_country = db_session.query(Country).filter_by(country_id=country.country_id).first()
    assert deleted_country is None

def test_delete_country_not_found(auth_admin, db_session):
    """
    Тестирует, что возвращается ошибка, если страна с таким ID не найдена.
    """
    non_existent_country_id = str(uuid.uuid4())

    response = auth_admin.delete(
        f"/api/admin_panel/countries/{non_existent_country_id}/delete",
        json={"acceptance": True},
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с таким ID не найдена"


def test_delete_country_invalid_id(auth_admin):
    """
    Тестирует, что возвращается ошибка, если ID страны имеет неверный формат.
    """
    invalid_country_id = "invalid-id"

    response = auth_admin.delete(
        f"/api/admin_panel/countries/{invalid_country_id}/delete",
        json={"acceptance": True},
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у страны"


def test_delete_country_acceptance_missing(auth_admin, country):
    """
    Тестирует, что возвращается ошибка, если acceptance не установлен.
    """
    response = auth_admin.delete(
        f"/api/admin_panel/countries/{country.country_id}/delete",
        json={"acceptance": None},
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == (
        "Если вы хотите удалить данную страну, "
        "вам необходимо поставить галочку выше"
    )

def test_add_tour_unauthorized(auth_moderator, valid_tour_data):
    """
    Тест добавления тура без авторизации.
    """
    valid_tour_data["cover_image"] = (BytesIO(b"fake image data"), "cover.jpg")

    response = auth_moderator.post(
        "api/admin_panel/tours/new",
        data=valid_tour_data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data["success"] is False
    assert response_data["message"] == "Неизвестный пользователь!"


def test_add_tour_invalid_data(auth_admin, valid_tour_data):
    """
    Тест добавления тура с некорректными данными.
    """
    del valid_tour_data["tour_title"]
    valid_tour_data["cover_image"] = (BytesIO(b"fake image data"), "cover.jpg")

    response = auth_admin.post(
        "api/admin_panel/tours/new",
        data=valid_tour_data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data["success"] is False
    assert "errors" in response_data

def test_show_tour_edit_page_success(auth_admin, db_session, tour):
    """
    Тестирует успешное получение данных о туре для страницы редактирования.
    """
    response = auth_admin.get(f'api/admin_panel/tours/{tour.tour_id}/edit')

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["tour"]["tour_title"] == tour.tour_title
    assert data["tour"]["tour_description"] == tour.tour_description
    assert data["tour"]["tour_text"] == tour.tour_text
    assert str(data["tour"]["tour_id"]) == str(tour.tour_id)


def test_show_tour_edit_page_tour_not_found(auth_admin, db_session):
    """
    Тестирует сценарий, когда тур с данным ID не найден.
    """
    invalid_tour_id = str(uuid.uuid4())

    response = auth_admin.get(f'api/admin_panel/tours/{invalid_tour_id}/edit')

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Тур с таким ID не найден"


def test_show_tour_edit_page_invalid_id_format(auth_admin, db_session):
    """
    Тестирует сценарий, когда ID тура имеет неверный формат.
    """
    invalid_tour_id = "invalid-uuid-format"

    response = auth_admin.get(f'api/admin_panel/tours/{invalid_tour_id}/edit')

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у тура"

def test_show_tour_edit_page_forbidden_for_non_admin(auth_moderator, db_session, tour):
    """
    Тестирует сценарий, когда пользователь с ролью модератора пытается получить доступ.
    """
    response = auth_moderator.get(f'api/admin_panel/tours/{tour.tour_id}/edit')

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неизвестный пользователь!"

def test_edit_tour_invalid_id_format(auth_admin, db_session):
    """
    Тестирует обновление тура с некорректным форматом ID.
    """
    invalid_tour_id = "invalid-uuid-format"

    updated_data = {
        "tour_title": "Updated Tour Title",
        "tour_description": "Updated Description",
        "tour_text": "Updated Text",
        "tour_price": "500"
    }

    response = auth_admin.put(f'api/admin_panel/tours/{invalid_tour_id}/edit', data=updated_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Неверный формат ID у тура"


def test_edit_tour_tour_not_found(auth_admin, db_session,category, country):
    """
    Тестирует обновление тура, которого нет в базе данных.
    """
    invalid_tour_id = str(uuid.uuid4())
    updated_data = {
        "tour_title": "Updated Tour Title",
        "tour_description": "Updated Description",
        "tour_text": "Updated Text",
        "tour_price": "500",
        "category_id": str(category.category_id),
        "country_id": str(country.country_id),
        "offer_id": None,
    }

    response = auth_admin.put(f'api/admin_panel/tours/{invalid_tour_id}/edit', data=updated_data)

    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Тур с таким ID не найден"


def test_edit_tour_category_not_found(auth_admin, db_session, tour):
    """
    Тестирует обновление тура с несуществующей категорией.
    """
    invalid_category_id = str(uuid.uuid4())

    updated_data = {
        "tour_title": "Updated Tour Title",
        "tour_description": "Updated Description",
        "tour_text": "Updated Text",
        "tour_price": "500",
        "category_id": invalid_category_id,
        "country_id": str(tour.country_id)
    }

    response = auth_admin.put(f'api/admin_panel/tours/{tour.tour_id}/edit', data=updated_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Категория с переданным UUID не найдена"


def test_edit_tour_country_not_found(auth_admin, db_session, tour):
    """
    Тестирует обновление тура с несуществующей страной.
    """
    invalid_country_id = str(uuid.uuid4())

    updated_data = {
        "tour_title": "Updated Tour Title",
        "tour_description": "Updated Description",
        "tour_text": "Updated Text",
        "tour_price": "500",
        "category_id": str(tour.category_id),
        "country_id": invalid_country_id
    }

    response = auth_admin.put(f'api/admin_panel/tours/{tour.tour_id}/edit', data=updated_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Страна с переданным UUID не найдена"

def test_edit_tour_forbidden_for_non_admin(auth_moderator, db_session, tour):
    """
    Тестирует попытку редактирования тура пользователем, который не является администратором.
    """
    updated_data = {
        "tour_title": "Updated Tour Title",
        "tour_description": "Updated Description",
        "tour_text": "Updated Text",
        "tour_price": "500"
    }

    response = auth_moderator.put(f'api/admin_panel/tours/{tour.tour_id}/edit', data=updated_data)

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неизвестный пользователь!"
