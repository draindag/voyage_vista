import pytest
from marshmallow.exceptions import ValidationError
from webapp.schemas.ReviewSchema import ReviewSchema
from webapp.models.Review import Review

def test_review_schema_serialization(review):
    """Тестирование корректной сериализации отзыва."""
    schema = ReviewSchema()
    serialized_data = schema.dump(review)

    assert "review_text" in serialized_data
    assert serialized_data["review_text"] == review.review_text
    assert "review_value" in serialized_data
    assert serialized_data["review_value"] == review.review_value
    assert "author" in serialized_data
    assert "tour" in serialized_data

def test_review_schema_deserialization(valid_review_data):
    """Тестирование корректной десериализации отзыва."""
    schema = ReviewSchema()
    deserialized_data = schema.load(valid_review_data)

    assert isinstance(deserialized_data, Review)
    assert deserialized_data.review_text == valid_review_data["review_text"]
    assert deserialized_data.review_value == valid_review_data["review_value"]
    assert deserialized_data.author_id == valid_review_data["author_id"]
    assert deserialized_data.tour_id == valid_review_data["tour_id"]

def test_review_schema_empty_text(valid_review_data):
    """Тестирование пустого текста отзыва."""
    schema = ReviewSchema()
    empty_text_data = valid_review_data.copy()
    empty_text_data['review_text'] = ""

    with pytest.raises(ValidationError) as exc_info:
        schema.load(empty_text_data)
    errors = exc_info.value.messages
    assert "review_text" in errors
    assert errors["review_text"] == ["Текст отзыва не должен быть пустым"]

def test_review_schema_invalid_review_value(valid_review_data):
    """Тестирование некорректной оценки отзыва."""
    schema = ReviewSchema()
    invalid_review_value_data = valid_review_data.copy()
    invalid_review_value_data['review_value'] = 6

    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_review_value_data)
    errors = exc_info.value.messages
    assert "review_value" in errors
    assert errors["review_value"] == ["Оценка должна быть целым числом в диапазоне от 1 до 5!"]

def test_review_schema_invalid_author_id(valid_review_data):
    """Тестирование некорректного UUID автора."""
    schema = ReviewSchema()
    invalid_author_id_data = valid_review_data.copy()
    invalid_author_id_data['author_id'] = "invalid-uuid"

    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_author_id_data)
    errors = exc_info.value.messages
    assert "author_id" in errors
    assert errors["author_id"] == ["Not a valid UUID."]

def test_review_schema_invalid_tour_id(valid_review_data):
    """Тестирование некорректного UUID тура."""
    schema = ReviewSchema()
    invalid_tour_id_data = valid_review_data.copy()
    invalid_tour_id_data['tour_id'] = "invalid-uuid"

    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_tour_id_data)
    errors = exc_info.value.messages
    assert "tour_id" in errors
    assert errors["tour_id"] == ["Not a valid UUID."]