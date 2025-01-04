import pytest

from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from datetime import datetime
from decimal import Decimal

from webapp import db
from webapp.models.Tour import Tour
from webapp.models.Reply import Reply


@pytest.mark.usefixtures("db_session")
def test_tour_creation(category, tour):
    """Тестирование создания тура."""
    assert tour.tour_id is not None
    assert tour.tour_title == "Sample Tour"
    assert tour.tour_description == "Sample description"
    assert tour.category_id == category.category_id


@pytest.mark.usefixtures("db_session")
def test_unique_tour_title_in_category(category, tour, country):
    """Проверка уникальности заголовка тура в рамках одной категории."""
    tour1 = Tour(
        tour_title="Sample Tour",
        tour_description="Another description",
        tour_text="More details...",
        tour_price=200.0,
        tour_start_date=datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
        tour_end_date=datetime.strptime("2024-03-05", "%Y-%m-%d").date(),
        category_id=category.category_id,
        country_id=country.country_id
    )

    db.session.add(tour1)
    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


@pytest.mark.usefixtures("db_session")
def test_price_with_discount(category, tour, offer):
    """Тестирование метода get_price_with_discount."""
    tour.offers.append(offer)
    db.session.commit()

    assert tour.get_price_with_discount() == Decimal("160.00")


def test_tour_replies_property(db_session, category, tour, reply):
    """Тестирование свойства tour_replies."""
    reply1 = Reply(
        reply_text="Can't wait to try it!",
        author_id=uuid4(),
        tour_id=tour.tour_id,
        parent_reply_id=reply.reply_id
    )
    db.session.add(reply1)
    db.session.commit()

    tour_replies = tour.tour_replies.all()

    assert reply in tour_replies, "Ответ верхнего уровня отсутствует в tour_replies"
    assert reply1 not in tour_replies, "Дочерний ответ оказался в tour_replies"

