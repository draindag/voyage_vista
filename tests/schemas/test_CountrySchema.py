import pytest
from marshmallow.exceptions import ValidationError
from webapp.schemas.CountrySchema import CountrySchema
from webapp.models.Country import Country

def test_country_schema_serialization(country):
    """Тестирование сериализации правильных данных."""
    schema = CountrySchema()
    serialized_data = schema.dump(country)

    assert "country_name" in serialized_data
    assert serialized_data["country_name"] == country.country_name
    assert "country_description" in serialized_data
    assert serialized_data["country_description"] == country.country_description

def test_country_schema_deserialization(valid_country_data):
    """Тестирование десериализации правильных данных."""
    schema = CountrySchema()
    deserialized_data = schema.load(valid_country_data)

    assert isinstance(deserialized_data, Country)
    assert deserialized_data.country_name == valid_country_data["country_name"]
    assert deserialized_data.country_description == valid_country_data["country_description"]

def test_country_schema_required_fields():
    """Тестирование обязательных полей."""
    schema = CountrySchema()

    # Тестируем отсутствие country_name
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "country_description": "A description of the country"
        })
    assert "country_name" in exc_info.value.messages

    # Тестируем отсутствие country_description
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "country_name": "Country Name"
        })
    assert "country_description" in exc_info.value.messages

def test_country_schema_validate_name():
    """Тестирование валидации поля country_name."""
    schema = CountrySchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "country_name": "",
            "country_description": "A description of the country"
        })
    assert "Название страны не должно быть пустым" in str(exc_info.value)

    # Слишком длинное имя
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "country_name": "A" * 31,
            "country_description": "A description of the country"
        })
    assert "Название страны должно содержать не более 30 символов" in str(exc_info.value)

def test_country_schema_validate_description():
    """Тестирование валидации поля country_description."""
    schema = CountrySchema()

    # Пустое описание
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "country_name": "Country Name",
            "country_description": ""
        })
    assert "Описание страны не должно быть пустым" in str(exc_info.value)

def test_country_schema_empty_fields():
    """Тестирование обработки пустых обязательных полей."""
    schema = CountrySchema()

    # Пустые значения для всех полей
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "country_name": "",
            "country_description": ""
        })
    assert "country_name" in exc_info.value.messages
    assert "country_description" in exc_info.value.messages
