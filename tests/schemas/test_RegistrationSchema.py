import pytest

from marshmallow.exceptions import ValidationError
from webapp.schemas.RegistrationSchema import RegistrationSchema

def test_registration_schema_missing_fields():
    """Тестирование пропущенных обязательных полей."""
    schema = RegistrationSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({})
    errors = exc_info.value.messages
    assert "login" in errors
    assert "email" in errors
    assert "password" in errors
    assert "password_repeat" in errors


def test_registration_schema_invalid_email():
    """Тестирование некорректного email."""
    schema = RegistrationSchema()
    invalid_data = {
        "login": "testuser",
        "email": "invalid-email",
        "password": "securepassword",
        "password_repeat": "securepassword"
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_data)
    assert "email" in exc_info.value.messages


def test_registration_schema_empty_or_long_login():
    """Тестирование пустого или слишком длинного логина."""
    schema = RegistrationSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "login": "",
            "email": "testuser@example.com",
            "password": "securepassword",
            "password_repeat": "securepassword"
        })
    assert "login" in exc_info.value.messages

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "login": "a" * 31,
            "email": "testuser@example.com",
            "password": "securepassword",
            "password_repeat": "securepassword"
        })
    assert "login" in exc_info.value.messages

def test_registration_schema_empty_password():
    """Тестирование пустого пароля."""
    schema = RegistrationSchema()
    invalid_data = {
        "login": "testuser",
        "email": "testuser@example.com",
        "password": "",
        "password_repeat": ""
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_data)
    assert "Пароль не может быть пустым" in str(exc_info.value)

def test_registration_schema_password_mismatch(invalid_registration_data):
    """Тестирование несовпадающих паролей."""
    schema = RegistrationSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_registration_data)
    assert "Пароли должны совпадать!" in str(exc_info.value)
