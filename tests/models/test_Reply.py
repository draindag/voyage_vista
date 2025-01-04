import pytest

from sqlalchemy.exc import IntegrityError

from webapp import db
from webapp.models.Reply import Reply

def test_reply_creation(reply):
    """Тестирование создания ответа."""
    assert reply.reply_text == "Great tour!"
    assert reply.author_id is not None
    assert reply.tour_id is not None
    assert reply.reply_id is not None

@pytest.mark.usefixtures("db_session")
def test_reply_text_required(user, tour):
    """Тестирование обязательности текста ответа."""
    reply = Reply(
        reply_text=None,
        author_id=user.user_id,
        tour_id=tour.tour_id
    )

    db.session.add(reply)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_reply_with_child_reply(reply, child_reply):
    """Тестирование вложенных ответов."""
    assert len(reply.replies) == 1
    assert child_reply in reply.replies
    assert child_reply.parent_reply_id == reply.reply_id

def test_reply_deletion(reply, child_reply):
    """Тестирование удаления ответа и каскадного удаления вложенных ответов."""
    db.session.delete(reply)
    db.session.commit()

    assert db.session.query(Reply).filter(Reply.reply_id == child_reply.reply_id).first() is None

def test_reply_without_parent(reply):
    """Тестирование ответа без родительского ответа."""
    reply_without_parent = Reply(
        reply_text="This is a standalone reply.",
        author_id=reply.author_id,
        tour_id=reply.tour_id
    )
    db.session.add(reply_without_parent)
    db.session.commit()

    assert reply_without_parent.parent_reply_id is None
