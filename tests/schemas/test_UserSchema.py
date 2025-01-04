import pytest
from marshmallow.exceptions import ValidationError
from webapp.schemas.UserSchema import UserSchema
from webapp.models.User import User


def test_user_schema_serialization(user):
    """Тестирование корректной сериализации пользователя."""
    schema = UserSchema()
    serialized_data = schema.dump(user)

    assert "login" in serialized_data
    assert serialized_data["login"] == user.login
    assert "email" in serialized_data
    assert serialized_data["email"] == user.email
    assert "fav_tours" in serialized_data
    assert "transactions" in serialized_data


def test_user_schema_deserialization(valid_user_data):
    """Тестирование корректной десериализации пользователя."""
    schema = UserSchema()
    deserialized_data = schema.load(valid_user_data)

    assert isinstance(deserialized_data, User)
    assert deserialized_data.login == valid_user_data["login"]
    assert deserialized_data.email == valid_user_data["email"]


def test_user_schema_missing_login():
    """Тестирование отсутствия логина."""
    schema = UserSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"email": "user@example.com"})
    errors = exc_info.value.messages
    assert "login" in errors
    assert errors["login"] == ["Поле 'Логин' обязательно для заполнения"]


def test_user_schema_missing_email():
    """Тестирование отсутствия email."""
    schema = UserSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"login": "testuser"})
    errors = exc_info.value.messages
    assert "email" in errors
    assert errors["email"] == ["Поле 'Email' обязательно для заполнения"]


def test_user_schema_invalid_email():
    """Тестирование некорректного email."""
    schema = UserSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"login": "testuser", "email": "invalid-email"})
    errors = exc_info.value.messages
    assert "email" in errors
    assert errors["email"] == ["Not a valid email address."]

