import pytest

from marshmallow.exceptions import ValidationError
from webapp.schemas.LoginSchema import LoginSchema

def test_login_schema_deserialization(valid_login_data):
    """Тестирование десериализации правильных данных."""
    schema = LoginSchema()
    deserialized_data = schema.load(valid_login_data)
    assert deserialized_data["email"] == valid_login_data["email"]
    assert deserialized_data["password"] == valid_login_data["password"]

def test_login_schema_required_fields():
    """Тестирование обязательных полей."""
    schema = LoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "password": "securepassword"
        })
    assert "Поле 'Email' обязательно для заполнения" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "email": "user@example.com"
        })
    assert "Поле 'Пароль' обязательно для заполнения" in str(exc_info.value)

def test_login_schema_invalid_email():
    """Тестирование валидации поля email."""
    schema = LoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "email": "invalid-email",
            "password": "securepassword"
        })
    assert "Некорректный адрес электронной почты" in str(exc_info.value)

def test_login_schema_empty_password():
    """Тестирование валидации пустого пароля."""
    schema = LoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "email": "user@example.com",
            "password": "   "
        })
    assert "Пароль не может быть пустым" in str(exc_info.value)
