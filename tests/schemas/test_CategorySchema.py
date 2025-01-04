import pytest
from marshmallow.exceptions import ValidationError
from webapp.schemas.CategorySchema import CategorySchema
from webapp.models.Category import Category

def test_category_schema_serialization(category):
    """Тестирование корректной сериализации."""
    schema = CategorySchema()
    serialized_data = schema.dump(category)

    assert "category_title" in serialized_data
    assert serialized_data["category_title"] == category.category_title
    assert "category_description" in serialized_data
    assert serialized_data["category_description"] == category.category_description

def test_category_schema_deserialization(valid_category_data):
    """Тестирование корректной десериализации."""
    schema = CategorySchema()
    deserialized_data = schema.load(valid_category_data)

    assert isinstance(deserialized_data, Category)
    assert deserialized_data.category_title == valid_category_data["category_title"]
    assert deserialized_data.category_description == valid_category_data["category_description"]

def test_category_schema_empty_title():
    """Тестирование пустого названия категории."""
    schema = CategorySchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "category_title": "",
            "category_description": "Valid description"})
    errors = exc_info.value.messages
    assert "category_title" in errors
    assert errors["category_title"] == ["Название категории не должно быть пустым"]

def test_category_schema_long_title(valid_category_data):
    """Тестирование слишком длинного названия категории."""
    schema = CategorySchema()
    long_title_data = {
        "category_title": "A" * 31,
        "category_description": valid_category_data["category_description"]
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(long_title_data)
    errors = exc_info.value.messages
    assert "category_title" in errors
    assert errors["category_title"] == ["Название категории должно содержать не более 30 символов"]

def test_category_schema_empty_description():
    """Тестирование пустого описания категории."""
    schema = CategorySchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"category_title": "Valid title", "category_description": ""})
    errors = exc_info.value.messages
    assert "category_description" in errors
    assert errors["category_description"] == ["Описание категории не должно быть пустым"]

