import pytest

from sqlalchemy.exc import IntegrityError

from webapp import db
from webapp.models.Review import Review

def test_review_creation(review):
    """Тестирование создания отзыва."""
    assert review.review_text == "This was a fantastic tour!"
    assert review.review_value == 5
    assert review.author_id is not None
    assert review.tour_id is not None
    assert review.review_id is not None

@pytest.mark.usefixtures("db_session")
def test_review_text_required(user, tour):
    """
    Тестирование обязательности текста отзыва.
    Замечание: пустой отзыв создать можно review_text=""
    """
    review = Review(
        review_text=None,
        review_value=5,
        author_id=user.user_id,
        tour_id=tour.tour_id
    )

    db.session.add(review)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_review_author_and_tour_relationship(review, user, tour):
    """Тестирование связи отзыва с автором и туром."""
    assert review.author_id == user.user_id
    assert review.tour_id == tour.tour_id
