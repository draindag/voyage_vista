import pytest

from marshmallow.exceptions import ValidationError
from webapp.schemas.EditLoginSchema import EditLoginSchema

def test_edit_login_schema_deserialization(valid_edit_login_data):
    """Тестирование десериализации правильных данных."""
    schema = EditLoginSchema()
    deserialized_data = schema.load(valid_edit_login_data)
    assert deserialized_data["new_login"] == valid_edit_login_data["new_login"]
    assert deserialized_data["password"] == valid_edit_login_data["password"]

def test_edit_login_schema_required_fields():
    """Тестирование обязательных полей."""
    schema = EditLoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "password": "securepassword"
        })
    assert "Поле 'Логин' обязательно для заполнения" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "new_login": "newuser123"
        })
    assert "Поле 'Пароль' обязательно для заполнения" in str(exc_info.value)

def test_edit_login_schema_empty_new_login():
    """Тестирование валидации пустого логина."""
    schema = EditLoginSchema()

    # Пустой логин
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "new_login": "   ",
            "password": "securepassword"
        })
    assert "Поле 'Логин' не должно быть пустым" in str(exc_info.value)

def test_edit_login_schema_new_login_length():
    """Тестирование валидации длины логина."""
    schema = EditLoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "new_login": "a" * 31,
            "password": "securepassword"
        })
    assert "Поле 'Логин' должно содержать не более 30 символов" in str(exc_info.value)

def test_edit_login_schema_empty_password():
    """Тестирование валидации пустого пароля."""
    schema = EditLoginSchema()

    # Пустой пароль
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "new_login": "newuser123",
            "password": "   "
        })
    assert "Пароль не может быть пустым" in str(exc_info.value)
