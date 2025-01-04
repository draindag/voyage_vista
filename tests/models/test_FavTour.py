import pytest
from webapp import db

from webapp.models.FavTour import fav_tours


@pytest.mark.usefixtures("db_session")
def test_add_favorite_tour(user, tour):
    """Тестирование добавления тура в избранное."""
    db.session.execute(fav_tours.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    result = db.session.execute(fav_tours.select().where(
        (fav_tours.c.tour_id == tour.tour_id) & (fav_tours.c.user_id == user.user_id)
    )).fetchone()

    assert result is not None
    assert result.tour_id == tour.tour_id
    assert result.user_id == user.user_id


@pytest.mark.usefixtures("db_session")
def test_remove_favorite_tour(user, tour):
    """Тестирование удаления тура из избранного."""
    db.session.execute(fav_tours.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    db.session.execute(fav_tours.delete().where(
        (fav_tours.c.tour_id == tour.tour_id) & (fav_tours.c.user_id == user.user_id)
    ))
    db.session.commit()

    result = db.session.execute(fav_tours.select().where(
        (fav_tours.c.tour_id == tour.tour_id) & (fav_tours.c.user_id == user.user_id)
    )).fetchone()

    assert result is None


@pytest.mark.usefixtures("db_session")
def test_favorite_tour_cascade_delete_user(user, tour):
    """Тестирование каскадного удаления при удалении пользователя."""
    db.session.execute(fav_tours.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    result = db.session.execute(fav_tours.select().where(
        fav_tours.c.tour_id == tour.tour_id
    )).fetchone()

    assert result is None


@pytest.mark.usefixtures("db_session")
def test_favorite_tour_cascade_delete_tour(user, tour):
    """Тестирование каскадного удаления при удалении тура."""
    db.session.execute(fav_tours.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    db.session.delete(tour)
    db.session.commit()

    result = db.session.execute(fav_tours.select().where(
        fav_tours.c.user_id == user.user_id
    )).fetchone()

    assert result is None
