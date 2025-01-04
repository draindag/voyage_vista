import pytest

from sqlalchemy.exc import IntegrityError
from datetime import datetime

from webapp import db
from webapp.models.Country import Country
from webapp.models.Tour import Tour


@pytest.mark.usefixtures("db_session")
def test_country_creation(country):
    """Тестирование создания страны."""
    assert country.country_id is not None
    assert country.country_name == "Switzerland"
    assert country.country_description == "Known for its beautiful mountains, lakes, and resorts."

@pytest.mark.usefixtures("db_session")
def test_unique_country_name(country):
    """Проверка уникальности названия страны."""
    country1 = Country(
        country_name="Switzerland",
        country_description="A different description but same name"
    )

    db.session.add(country1)

    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

@pytest.mark.usefixtures("db_session")
def test_country_relationship_with_tours(category, country, tour):
    """Тестирование связи между странами и турами."""
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

    assert country.tours.count() == 2
    assert tour in country.tours
    assert tour1 in country.tours

