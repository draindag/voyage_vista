"""
Конфигурации и фикстуры для тестов
"""

import sys
import os

import pytest
from flask_jwt_extended import create_access_token

from datetime import datetime, date
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask-backend')))

from webapp import db
from webapp.app import create_app
from webapp.models.Category import Category
from webapp.models.Tour import Tour
from webapp.models.Country import Country
from webapp.models.SpecialOffer import SpecialOffer
from webapp.models.Reply import Reply
from webapp.models.Review import Review
from webapp.models.User import User


@pytest.fixture
def app():
    """
    Фикстура для создания приложения Flask.
    Используется для всех тестов, чтобы избежать повторного создания приложения.
    """
    return create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

@pytest.fixture
def client(app):
    """
    Фикстура для создания клиента Flask.
    Использует приложение, созданное в фикстуре `app`.
    """
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_session(app):
    """
    Фикстура для управления сессией базы данных.
    Создает схему базы данных перед каждым тестом и удаляет ее после.
    """
    # Создаем контекст приложения
    with app.app_context():
        # Создаем таблицы
        db.create_all()

        yield db.session

        db.session.remove()
        db.drop_all()

@pytest.fixture
def category(db_session):
    """Фикстура для создания категории."""
    category = Category(
        category_title="Adventure",
        category_description="Exciting and thrilling tours"
    )
    db.session.add(category)
    db.session.commit()
    return category

@pytest.fixture
def country(db_session):
    """Фикстура для создания страны."""
    country = Country(
        country_name="Switzerland",
        country_description="Known for its beautiful mountains, lakes, and resorts."
    )
    db.session.add(country)
    db.session.commit()
    return country

@pytest.fixture
def tour(db_session, category, country):
    """Фикстура для создания тура."""
    tour = Tour(
        tour_title="Sample Tour",
        tour_description="Sample description",
        tour_text="Detailed description...",
        tour_price=Decimal("200.0"),
        tour_start_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        tour_end_date=datetime.strptime("2024-01-10", "%Y-%m-%d").date(),
        category_id=category.category_id,
        country_id=country.country_id
    )
    db.session.add(tour)
    db.session.commit()
    return tour

@pytest.fixture
def offer(db_session):
    """Фикстура для создания специального предложения."""
    offer = SpecialOffer(
        offer_title="Sample Discount",
        discount_size=20.0,
        end_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date()
    )
    db.session.add(offer)
    db.session.commit()
    return offer

@pytest.fixture
def user(db_session):
    """Фикстура для создания пользователя."""
    user = User(
        login="testuser",
        email="testuser@example.com",
        password="password123"
    )
    user.set_password("password123")  # Задаем пароль для пользователя
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def moderator(db_session):
    """Фикстура для создания пользователя."""
    user = User(
        login="moderator",
        email="moderator@example.com",
        password="password123",
        role="moderator"
    )
    user.set_password("password123")  # Задаем пароль для пользователя
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def reply(db_session, tour, user):
    """Фикстура для создания ответов."""
    reply = Reply(
        reply_text="Great tour!",
        author_id=user.user_id,
        tour_id=tour.tour_id
    )
    db.session.add(reply)
    db.session.commit()
    return reply

@pytest.fixture
def child_reply(db_session, user, tour, reply):
    """Фикстура для создания вложенного ответа."""
    child_reply = Reply(
        reply_text="This is a child reply.",
        author_id=user.user_id,
        tour_id=tour.tour_id,
        parent_reply_id=reply.reply_id
    )
    db.session.add(child_reply)
    db.session.commit()
    return child_reply

@pytest.fixture
def review(db_session, user, tour):
    """Фикстура для создания отзыва."""
    review = Review(
        review_text="This was a fantastic tour!",
        review_value=5,
        author_id=user.user_id,
        tour_id=tour.tour_id
    )
    db.session.add(review)
    db.session.commit()
    return review

@pytest.fixture
def valid_registration_data():
    return {
        "login": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
        "password_repeat": "securepassword"
    }

@pytest.fixture
def invalid_registration_data():
    return {
        "login": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
        "password_repeat": "differentpassword"
    }

@pytest.fixture
def valid_category_data():
    """Корректные данные категории."""
    return {
        "category_title": "Nature",
        "category_description": "Tours related to nature exploration."
    }

@pytest.fixture
def valid_country_data():
    """Корректные данные страны."""
    return {
        "country_name": "Country Name",
        "country_description": "A description of the country"
    }

@pytest.fixture
def valid_offer_data():
    return {
        "offer_title": "Summer Discount",
        "discount_size": 20.0,
        "end_date": '2024-01-10'
    }

@pytest.fixture
def valid_login_data():
    return {
        "email": "user@example.com",
        "password": "securepassword"
    }

@pytest.fixture
def valid_edit_login_data():
    return {
        "new_login": "newuser123",
        "password": "securepassword"
    }

@pytest.fixture
def valid_tour_data(category, country):
    return {
        'tour_title': 'Tour Title',
        'tour_description': 'Description of the tour',
        'tour_text': 'Detailed tour description...',
        'tour_price': Decimal('200.00'),
        'tour_start_date': '2024-01-01',
        'tour_end_date': '2024-01-10',
        'category_id': category.category_id,
        'country_id': country.country_id,
    }

@pytest.fixture
def valid_reply_data(tour, user):
    return {
        'reply_text': 'Great tour!',
        'author_id': user.user_id,
        'tour_id': tour.tour_id
    }

@pytest.fixture
def valid_review_data(tour, user):
    return {
        'review_text': 'This was a fantastic tour!',
        'review_value': 5,
        'author_id': user.user_id,
        'tour_id': tour.tour_id
    }

@pytest.fixture
def valid_user_data():
    return {
        "login": "testuser",
        "email": "user@example.com",
    }

@pytest.fixture
def setup_popular_tours(db_session, category, country, user):
    # Создаем тестовые туры
    tours = []
    for i in range(25):  # Создаем 25 туров для проверки постраничного вывода
        tour = Tour(
            tour_title=f"Tour {i}",
            tour_description="Description",
            tour_text="Tour text",
            tour_price=Decimal("100.0"),
            tour_start_date=datetime(2024, 1, 1).date(),
            tour_end_date=datetime(2024, 1, 10).date(),
            category_id=category.category_id,
            country_id=country.country_id
        )
        db_session.add(tour)
        tours.append(tour)

    db_session.commit()

    # Добавляем оценки (reviews) для каждого тура
    for i, tour in enumerate(tours):
        for j in range((i % 5) + 1):  # Условие для создания разного количества оценок
            review = Review(
                review_text="Review text",
                review_value=5 - (j % 5),  # Оценки 5, 4, 3, 2, 1
                tour_id=tour.tour_id,
                author_id=user.user_id,
            )
            db_session.add(review)

    db_session.commit()
    return tours

@pytest.fixture
def tours_with_category_and_offer_and_country(db_session, category,country, offer):
    for i in range(5):
        tour = Tour(
            tour_title=f"Tour {i}",
            tour_description="Description",
            tour_text="Tour text",
            tour_price=Decimal("100.0"),
            tour_start_date=datetime(2024, 1, 1).date(),
            tour_end_date=datetime(2024, 1, 10).date(),
            category_id=category.category_id,
            country_id=country.country_id
        )
        tour.offers.append(offer)
        db.session.add(tour)
    db.session.commit()

@pytest.fixture
def auth_client(client, user, db_session):
    """Фикстура для аутентифицированного клиента."""
    token = create_access_token(identity=user.login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    return client

@pytest.fixture
def auth_moderator(client, moderator, db_session):
    """Фикстура для аутентифицированного модератора."""
    token = create_access_token(identity=moderator.login)
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    return client


