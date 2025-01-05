import pytest
import os

from webapp import db
from webapp.models.Reply import Reply

from uuid import uuid4, UUID
from flask_jwt_extended import create_access_token

def test_show_categories(db_session, client, category):
    response = client.get("api/tours/categories")
    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0

def test_show_tours_with_discounts(client, db_session, tour, offer):
    tour.offers.append(offer)
    db.session.commit()

    response = client.get("/api/tours/special_offers")

    assert response.status_code == 200

    data = response.json

    assert data["success"] is True
    assert isinstance(data["tours"], list)
    assert len(data["tours"]) > 0

    assert "prev_page" in data
    assert "next_page" in data

    for tour_data in data["tours"]:
        assert "offers" in tour_data and len(tour_data["offers"]) > 0


def test_show_tours_with_discounts_pagination(client, tours_with_category_and_offer_and_country):
    """Тест на пагинацию туров по страницам."""
    response = client.get("/api/tours/special_offers?page=1")

    assert response.status_code == 200
    data = response.json
    assert len(data["tours"]) == 4
    assert data["prev_page"] is False
    assert data["next_page"] is True

    response = client.get("/api/tours/special_offers?page=2")

    assert response.status_code == 200
    data = response.json
    assert len(data["tours"]) == 1
    assert data["prev_page"] is True
    assert data["next_page"] is False

def test_show_most_popular_tours(client, setup_popular_tours):
    response = client.get("/api/tours/popular?page=1")
    assert response.status_code == 200

    data = response.json
    assert data["success"] is True
    assert len(data["tours"]) == 4
    assert data["prev_page"] is False
    assert data["next_page"] is True

    for tour in data["tours"]:
        assert "tour_id" in tour
        assert "tour_title" in tour
        assert "tour_description" in tour

    response = client.get("/api/tours/popular?page=5")
    assert response.status_code == 200

    data = response.json
    assert data["success"] is True
    assert len(data["tours"]) == 4
    assert data["prev_page"] is True
    assert data["next_page"] is False

@pytest.mark.parametrize("endpoint, param_name", [
    ("/api/tours/categories", "category_id"),
    ("/api/tours/countries", "country_id")
])
def test_show_page_success(client, endpoint, param_name, category, country, tours_with_category_and_offer_and_country):
    """Проверяем успешное получение туров для категории или страны."""
    valid_id = category.category_id if endpoint.endswith("categories") else country.country_id
    response = client.get(f"{endpoint}/{valid_id}?page=1")
    assert response.status_code == 200

    data = response.json
    assert data["success"] is True
    assert len(data["tours"]) == 4
    assert data["prev_page"] is False
    assert data["next_page"] is True


@pytest.mark.parametrize("endpoint, param_name", [
    ("/api/tours/categories", "Категория"),
    ("/api/tours/countries", "Страна")
])
def test_show_page_not_found(client, endpoint, param_name, db_session):
    """Проверяем случай, когда категория или страна не найдены."""
    invalid_id = uuid4()
    response = client.get(f"{endpoint}/{invalid_id}?page=1")
    assert response.status_code == 404

    data = response.json
    assert data["success"] is False
    assert data["message"] == f"{param_name} не найдена"


@pytest.mark.parametrize("endpoint, param_name", [
    ("/api/tours/categories", "категории"),
    ("/api/tours/countries", "страны")
])
def test_show_page_invalid_id(client, endpoint, param_name):
    """Проверяем случай, когда передан некорректный UUID."""
    invalid_id = "12345"
    response = client.get(f"{endpoint}/{invalid_id}?page=1")
    assert response.status_code == 400

    data = response.json
    assert data["success"] is False
    assert data["error"] == f"Неверный формат ID у {param_name}"


@pytest.mark.parametrize("endpoint, param_name", [
    ("/api/tours/categories", "category_id"),
    ("/api/tours/countries", "country_id")
])
def test_show_page_last_page(client, endpoint, param_name, tours_with_category_and_offer_and_country, category, country):
    """Проверяем последнюю страницу, где туров меньше, чем TOURS_PER_PAGE."""
    per_page = int(os.getenv("TOURS_PER_PAGE"))
    last_page = (5 // per_page) + 1

    valid_id = category.category_id if endpoint.endswith("categories") else country.country_id
    response = client.get(f"{endpoint}/{valid_id}?page={last_page}")
    assert response.status_code == 200

    data = response.json
    assert data["success"] is True
    assert len(data["tours"]) == 5 % per_page
    assert data["prev_page"] is True
    assert data["next_page"] is False


@pytest.mark.parametrize("endpoint, param_name", [
    ("/api/tours/categories", "category_id"),
    ("/api/tours/countries", "country_id")
])
def test_show_page_empty(client, endpoint, param_name, category, country):
    """Проверяем случай, когда у категории или страны нет туров."""
    valid_id = category.category_id if endpoint.endswith("categories") else country.country_id
    response = client.get(f"{endpoint}/{valid_id}?page=1")
    assert response.status_code == 200

    data = response.json
    assert data["success"] is True
    assert len(data["tours"]) == 0
    assert data["prev_page"] is False
    assert data["next_page"] is False

def test_show_tour_page_success(tour, auth_client, db_session):
    """Успешный запрос с существующим туром."""
    response = auth_client.get(f"/api/tours/{tour.tour_id}")
    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    assert data["tour"]["tour_title"] == tour.tour_title
    assert "tour_replies" in data

def test_show_tour_page_invalid_tour_id(auth_client):
    """Запрос с некорректным форматом tour_id."""
    invalid_tour_id = "invalid-uuid"
    response = auth_client.get(f"/api/tours/{invalid_tour_id}")
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Неверный формат ID у тура" in response.json["error"]

def test_show_tour_page_not_found(auth_client, db_session):
    """Запрос для несуществующего тура."""
    non_existent_tour_id = str(uuid4())
    response = auth_client.get(f"/api/tours/{non_existent_tour_id}")
    assert response.status_code == 404
    assert response.json["success"] is False
    assert "Тур не найден" in response.json["message"]

def test_show_tour_page_replies_pagination(tour, user, auth_client, db_session):
    """Проверка постраничности комментариев."""
    for i in range(15):
        reply = Reply(
            reply_text=f"Reply {i}",
            author_id=user.user_id,
            tour_id=tour.tour_id
        )
        db_session.add(reply)
    db_session.commit()

    response = auth_client.get(f"/api/tours/{tour.tour_id}?page=1")
    assert response.status_code == 200
    data = response.json
    assert len(data["tour_replies"]) == int(os.getenv("REPLIES_PER_PAGE"))
    assert data["next_page"] is True
    assert data["prev_page"] is False

    response = auth_client.get(f"/api/tours/{tour.tour_id}?page=2")
    data = response.json
    assert data["next_page"] is False
    assert data["prev_page"] is True


def test_add_or_unfavourite_tour(auth_client, tour):
    """Тест успешного добавления и удаления тура из избранного."""
    response = auth_client.post(f"/api/tours/{tour.tour_id}/to_favourite")
    assert response.status_code == 201
    data = response.json
    assert data["success"] is True
    assert data["message"] == "Тур успешно добавлен в избранное"

    response = auth_client.delete(f"/api/tours/{tour.tour_id}/out_of_favourite")
    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    assert data["message"] == "Тур успешно удален из избранного"


def test_add_or_unfavourite_user_not_found(client, tour, db_session):
    """Тест на случай, когда пользователь не найден (невалидный токен)."""
    user_login = "nonexistent_user"
    token = create_access_token(identity=user_login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"

    for route in ["/to_favourite", "/out_of_favourite"]:
        method = "DELETE" if route == "/out_of_favourite" else "POST"
        response = client.open(f"/api/tours/{tour.tour_id}{route}", method=method)

        assert response.status_code == 401
        data = response.json
        assert data["success"] is False
        assert data["message"] == "Пользователь не найден"


@pytest.mark.parametrize(
    "route, invalid_tour_id, expected_status_code, expected_error_message",
    [
        ("/to_favourite", "invalid_uuid", 400, "Неверный формат ID у тура"),
        ("/out_of_favourite", "invalid_uuid", 400, "Неверный формат ID у тура")
    ]
)
def test_add_or_unfavourite_invalid_tour_id(auth_client, route, invalid_tour_id, expected_status_code,
                                            expected_error_message):
    """Тест на случай, когда передан некорректный UUID для тура."""
    method = "DELETE" if route == "/out_of_favourite" else "POST"

    response = auth_client.open(f"/api/tours/{invalid_tour_id}{route}", method=method)

    assert response.status_code == expected_status_code
    data = response.json
    assert data["success"] is False
    assert data["error"] == expected_error_message


@pytest.mark.parametrize(
    "route, invalid_tour_id, expected_status_code, expected_message",
    [
        ("/to_favourite", uuid4(), 404, "Тур не найден"),
        ("/out_of_favourite", uuid4(), 404, "Тур не найден")
    ]
)
def test_add_or_unfavourite_tour_not_found(auth_client, route, invalid_tour_id, expected_status_code, expected_message):
    """Тест на случай, когда тур не найден в базе данных."""
    method = "DELETE" if route == "/out_of_favourite" else "POST"

    response = auth_client.open(f"/api/tours/{invalid_tour_id}{route}", method=method)

    assert response.status_code == expected_status_code
    data = response.json
    assert data["success"] is False
    assert data["message"] == expected_message

def test_show_tour_payment_info_success(tour, auth_client, db_session):
    """Успешный запрос с существующим туром."""
    response = auth_client.get(f"/api/tours/{tour.tour_id}/payment")
    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    assert data["tour"]["tour_title"] == tour.tour_title

def test_show_tour_payment_info_invalid_tour_id(auth_client):
    """Запрос с некорректным форматом tour_id."""
    invalid_tour_id = "invalid-uuid"
    response = auth_client.get(f"/api/tours/{invalid_tour_id}/payment")
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Неверный формат ID у тура" in response.json["error"]

def test_show_tour_payment_info_not_found(auth_client, db_session):
    """Запрос для несуществующего тура."""
    non_existent_tour_id = str(uuid4())
    response = auth_client.get(f"/api/tours/{non_existent_tour_id}/payment")
    assert response.status_code == 404
    assert response.json["success"] is False
    assert "Тур не найден" in response.json["message"]

def test_show_tour_payment_info_user_not_found(tour, client, db_session):
    """Запрос, когда пользователь отсутствует в базе данных."""
    user_login = "nonexistent_user"
    token = create_access_token(identity=user_login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"

    response = client.get(f"/api/tours/{tour.tour_id}/payment")
    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Пользователь не найден" in response.json["message"]


@pytest.mark.parametrize(
    "acceptance, expected_status_code, expected_message",
    [
        (True, 200, "Оплата прошла успешно!"),
        (False, 400, "Для совершения оплаты, вам необходимо поставить галочку выше"),
        (None, 400, "Для совершения оплаты, вам необходимо поставить галочку выше"),
    ]
)
def test_add_transaction_success_and_failure(auth_client, db_session, acceptance, expected_status_code,
                                             expected_message, tour):
    """Тест на успешную и неуспешную оплату."""
    json_data = {"acceptance": acceptance}
    response = auth_client.post(f"/api/tours/{tour.tour_id}/payment", json=json_data)

    assert response.status_code == expected_status_code
    assert response.json["success"] is (expected_status_code == 200)
    assert expected_message in response.json["message"]


def test_add_transaction_user_not_found(client, db_session, tour):
    """Тест для случая, когда пользователь не найден."""
    user_login = "nonexistent_user"
    token = create_access_token(identity=user_login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"

    json_data = {"acceptance": True}
    response = client.post(f"/api/tours/{tour.tour_id}/payment", json=json_data)

    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Пользователь не найден" in response.json["message"]


def test_add_transaction_invalid_tour_id(auth_client):
    """Тест для случая, когда передан некорректный формат ID у тура."""
    invalid_tour_id = "invalid-uuid"

    json_data = {"acceptance": True}
    response = auth_client.post(f"/api/tours/{invalid_tour_id}/payment", json=json_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Неверный формат ID у тура" in response.json["error"]


def test_add_transaction_tour_not_found(auth_client, db_session):
    """Тест для случая, когда тур не найден."""
    non_existent_tour_id = str(uuid4())

    json_data = {"acceptance": True}
    response = auth_client.post(f"/api/tours/{non_existent_tour_id}/payment", json=json_data)

    assert response.status_code == 404
    assert response.json["success"] is False
    assert "Тур не найден" in response.json["message"]


def test_add_review_success(auth_client, db_session, tour, valid_review_data):
    """Тест успешного добавления отзыва."""

    response = auth_client.post(f"/api/tours/{tour.tour_id}/add_review", json=valid_review_data)

    assert response.status_code == 201
    assert response.json["success"] is True
    assert "review" in response.json
    assert response.json["review"]["review_text"] == valid_review_data["review_text"]
    assert response.json["review"]["review_value"] == valid_review_data["review_value"]

def test_add_review_user_not_found(client, db_session, valid_review_data, tour):
    """Тест для случая, когда пользователь не найден."""
    user_login = "nonexistent_user"
    token = create_access_token(identity=user_login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"

    response = client.post(f"/api/tours/{tour.tour_id}/add_review", json=valid_review_data)

    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Пользователь не найден" in response.json["message"]

def test_add_review_invalid_tour_id(auth_client, valid_review_data):
    """Тест для случая, когда передан некорректный формат ID у тура."""
    invalid_tour_id = "invalid-uuid"

    response = auth_client.post(f"/api/tours/{invalid_tour_id}/add_review", json=valid_review_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Неверный формат ID у тура" in response.json["error"]

def test_add_review_tour_not_found(auth_client, db_session, valid_review_data):
    """Тест для случая, когда тур не найден."""
    non_existent_tour_id = uuid4()

    response = auth_client.post(f"/api/tours/{non_existent_tour_id}/add_review", json=valid_review_data)

    assert response.status_code == 404
    assert response.json["success"] is False
    assert "Тур не найден" in response.json["message"]

def test_add_review_validation_error(auth_client, db_session, tour, valid_review_data):
    """Тест для случая, когда отзыв не проходит валидацию."""
    valid_review_data["review_text"] = ""

    response = auth_client.post(f"/api/tours/{tour.tour_id}/add_review", json=valid_review_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "errors" in response.json
    assert "review_text" in response.json["errors"]

def test_add_reply_success(auth_client, db_session, valid_reply_data, tour):
    """Тест успешного добавления комментария."""
    response = auth_client.post(f"/api/tours/{tour.tour_id}/add_reply", json=valid_reply_data)

    assert response.status_code == 201
    assert response.json["success"] is True
    assert "reply" in response.json
    assert response.json["reply"]["reply_text"] == valid_reply_data["reply_text"]
    assert response.json["reply"]["author"]["login"] == "testuser"

def test_add_reply_user_not_found(client, db_session, valid_reply_data, tour):
    """Тест, когда пользователь не найден в базе данных."""
    user_login = "nonexistent_user"
    token = create_access_token(identity=user_login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"

    response = client.post(f"/api/tours/{tour.tour_id}/add_reply", json=valid_reply_data)

    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Пользователь не найден" in response.json["message"]

def test_add_reply_invalid_tour_id(auth_client, db_session, valid_reply_data):
    """Тест с некорректным форматом tour_id."""
    invalid_tour_id = "invalid-uuid"
    response = auth_client.post(f"/api/tours/{invalid_tour_id}/add_reply", json=valid_reply_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Неверный формат ID у тура" in response.json["error"]

def test_add_reply_tour_not_found(auth_client, db_session, valid_reply_data):
    """Тест с несуществующим туром."""
    non_existent_tour_id = uuid4()
    response = auth_client.post(f"/api/tours/{non_existent_tour_id}/add_reply", json=valid_reply_data)

    assert response.status_code == 404
    assert response.json["success"] is False
    assert "Тур не найден" in response.json["message"]

def test_add_reply_missing_reply_text(auth_client, db_session, tour, valid_reply_data):
    """Тест с отсутствующим текстом комментария."""
    valid_reply_data["reply_text"] = ""
    response = auth_client.post(f"/api/tours/{tour.tour_id}/add_reply", json=valid_reply_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "errors" in response.json
    assert "reply_text" in response.json["errors"]

def test_delete_reply_success(auth_moderator, db_session, reply):
    """Тест успешного удаления комментария модератором"""
    response = auth_moderator.delete(f"/api/tours/replies/{reply.reply_id}/delete")

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["message"] == "Комментарий успешно удалён!"

def test_delete_reply_not_a_moderator(auth_client, db_session, reply):
    """Тест, когда обычный пользователь пытается удалить комментарий"""
    response = auth_client.delete(f"api/tours/replies/{reply.reply_id}/delete")

    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Неизвестный пользователь!"

def test_delete_reply_comment_not_found(auth_moderator, db_session):
    """Тест, когда комментарий с таким ID не найден"""
    invalid_reply_id = uuid4()
    response = auth_moderator.delete(f"/api/tours/replies/{invalid_reply_id}/delete")

    assert response.status_code == 404
    assert response.json["success"] is False
    assert response.json["message"] == "Комментарий с таким ID не найден"

def test_delete_reply_invalid_id_format(auth_moderator, db_session):
    """Тест, когда ID комментария имеет неверный формат"""
    invalid_reply_id = "invalid-uuid"
    response = auth_moderator.delete(f"api/tours/replies/{invalid_reply_id}/delete")

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["error"] == "Неверный формат ID у комментария"
