import pytest

from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from webapp import db
from webapp.models.User import User

@pytest.mark.usefixtures("db_session")
def test_user_creation(user):
    """Тестирование создания пользователя."""
    assert user.user_id is not None
    assert user.login == "testuser"
    assert user.email == "testuser@example.com"
    assert check_password_hash(user.password, "password123")

@pytest.mark.usefixtures("db_session")
def test_user_check_password(user):
    """Проверка правильности пароля пользователя."""

    assert user.check_password("password123") is True

    assert user.check_password("wrongpassword") is False

@pytest.mark.usefixtures("db_session")
def test_user_change_login(user):
    """Проверка изменения логина пользователя."""
    user.set_login("newlogin")
    db.session.commit()

    assert user.login == "newlogin"

@pytest.mark.usefixtures("db_session")
def test_user_change_email(user):
    """Проверка изменения email пользователя."""
    user.set_email("newemail@example.com")
    db.session.commit()

    assert user.email == "newemail@example.com"

@pytest.mark.usefixtures("db_session")
def test_set_moderator_role(user):
    """Проверка установки роли 'moderator'."""
    assert user.role == "visitor"

    user.set_moderator_role()
    db.session.commit()

    assert user.role == "moderator"

@pytest.mark.usefixtures("db_session")
def test_user_role_constraint():
    """Тестирование ограничения на роли пользователей."""
    user = User(
        login="testuser",
        email="testuser@example.com",
        password="password123",
        role="invalidrole"
    )

    db.session.add(user)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

@pytest.mark.usefixtures("db_session")
def test_user_relationship_with_reviews_and_replies(user, review, reply):
    """Тестирование связей пользователя с отзывами и ответами."""
    assert len(user.reviews.all()) == 1
    assert review in user.reviews.all()

    assert len(user.replies.all()) == 1
    assert reply in user.replies.all()

@pytest.mark.usefixtures("db_session")
def test_user_unique_email_and_login(user):
    """Тестирование уникальности email и login пользователя."""
    user1 = User(
        login="anotheruser",
        email="testuser@example.com",
        password="password123"
    )
    user1.set_password("password123")
    db.session.add(user1)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()

@pytest.mark.usefixtures("db_session")
def test_user_unique_login(user):
    user1 = User(
        login="testuser",
        email="user3@example.com",
        password="password123"
    )
    user1.set_password("password123")
    db.session.add(user1)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()