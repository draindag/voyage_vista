import pytest

from sqlalchemy.exc import IntegrityError

from webapp import db
from webapp.models.OffersAndTours import offers_tours


@pytest.mark.usefixtures("db_session")
def test_offer_tour_creation(tour, offer):
    """Тестирование создания связи между туром и предложением."""
    db.session.execute(offers_tours.insert().values(tour_id=tour.tour_id, offer_id=offer.offer_id))
    db.session.commit()

    result = db.session.execute(
        offers_tours.select().where(
            (offers_tours.c.tour_id == tour.tour_id) &
            (offers_tours.c.offer_id == offer.offer_id)
        )
    ).fetchone()

    assert result is not None
    assert result.tour_id == tour.tour_id
    assert result.offer_id == offer.offer_id


@pytest.mark.usefixtures("db_session")
def test_offer_tour_uniqueness(tour, offer):
    """Тестирование уникальности связи между туром и предложением."""
    db.session.execute(offers_tours.insert().values(tour_id=tour.tour_id, offer_id=offer.offer_id))
    db.session.commit()

    with pytest.raises(IntegrityError):
        db.session.execute(offers_tours.insert().values(tour_id=tour.tour_id, offer_id=offer.offer_id))
        db.session.commit()
    db.session.rollback()


@pytest.mark.usefixtures("db_session")
def test_offer_tour_cascade_delete(tour, offer):
    """Тестирование каскадного удаления при удалении тура или предложения."""
    db.session.execute(offers_tours.insert().values(tour_id=tour.tour_id, offer_id=offer.offer_id))
    db.session.commit()

    db.session.delete(tour)
    db.session.commit()

    result = db.session.execute(
        offers_tours.select().where(
            (offers_tours.c.tour_id == tour.tour_id) &
            (offers_tours.c.offer_id == offer.offer_id)
        )
    ).fetchone()

    assert result is None
