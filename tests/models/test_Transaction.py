import pytest

from sqlalchemy.exc import IntegrityError

from webapp import db
from webapp.models.Transaction import transactions

@pytest.mark.usefixtures("db_session")
def test_add_transaction(user, tour):
    """Тестирование добавления транзакции."""
    db.session.execute(transactions.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    result = db.session.execute(transactions.select().where(
        (transactions.c.tour_id == tour.tour_id) & (transactions.c.user_id == user.user_id)
    )).fetchone()

    assert result is not None
    assert result.tour_id == tour.tour_id
    assert result.user_id == user.user_id


@pytest.mark.usefixtures("db_session")
def test_remove_transaction(user, tour):
    """Тестирование удаления транзакции."""
    db.session.execute(transactions.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    db.session.execute(transactions.delete().where(
        (transactions.c.tour_id == tour.tour_id) & (transactions.c.user_id == user.user_id)
    ))
    db.session.commit()

    result = db.session.execute(transactions.select().where(
        (transactions.c.tour_id == tour.tour_id) & (transactions.c.user_id == user.user_id)
    )).fetchone()

    assert result is None


@pytest.mark.usefixtures("db_session")
def test_transaction_uniqueness(user, tour):
    """Тестирование уникальности транзакции."""
    db.session.execute(transactions.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    with pytest.raises(IntegrityError):
        db.session.execute(transactions.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
        db.session.commit()
    db.session.rollback()

@pytest.mark.usefixtures("db_session")
def test_transaction_cascade_delete_user(user, tour):
    """Тестирование каскадного удаления транзакций при удалении пользователя."""
    db.session.execute(transactions.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    result = db.session.execute(transactions.select().where(
        transactions.c.tour_id == tour.tour_id
    )).fetchone()

    assert result is None


@pytest.mark.usefixtures("db_session")
def test_transaction_cascade_delete_tour(user, tour):
    """Тестирование каскадного удаления транзакций при удалении тура."""
    db.session.execute(transactions.insert().values(tour_id=tour.tour_id, user_id=user.user_id))
    db.session.commit()

    db.session.delete(tour)
    db.session.commit()

    result = db.session.execute(transactions.select().where(
        transactions.c.user_id == user.user_id
    )).fetchone()

    assert result is None
