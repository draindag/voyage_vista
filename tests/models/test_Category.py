import pytest

from sqlalchemy.exc import IntegrityError
from datetime import datetime

from webapp import db
from webapp.models.Category import Category
from webapp.models.Tour import Tour

@pytest.mark.usefixtures("db_session")
def test_category_creation(category):
    """Тестирование создания категории."""
    db.session.add(category)
    db.session.commit()
    assert category.category_id is not None
    assert category.category_title == "Adventure"
    assert category.category_description == "Exciting and thrilling tours"


@pytest.mark.usefixtures("db_session")
def test_unique_category_title(category):
    """Проверка уникальности заголовка категории."""
    category1 = Category(
        category_title="Adventure",
        category_description="Different description but same title"
    )

    db.session.add(category1)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


@pytest.mark.usefixtures("db_session")
def test_category_relationship_with_tours(category, tour, country):
    """Тестирование связи между категориями и турами."""
    tour1 = Tour(
        tour_title="Rome Tour",
        tour_description="Explore the ancient city of Rome",
        tour_text="A detailed itinerary of the Rome city tour...",
        tour_price=150.0,
        tour_start_date=datetime.strptime("2024-05-01", "%Y-%m-%d").date(),
        tour_end_date=datetime.strptime("2024-05-10", "%Y-%m-%d").date(),
        category_id=category.category_id,
        country_id=country.country_id
    )

    db.session.add(tour1)
    db.session.commit()

    assert category.tours.count() == 2
    assert tour in category.tours
    assert tour1 in category.tours


