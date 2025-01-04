import pytest

from datetime import date

from marshmallow.exceptions import ValidationError
from webapp.schemas.OfferSchema import OfferSchema
from webapp.models.SpecialOffer import SpecialOffer


def test_offer_schema_serialization(offer):
    """Тестирование сериализации правильных данных."""
    schema = OfferSchema()
    serialized_data = schema.dump(offer)

    assert "offer_title" in serialized_data
    assert serialized_data["offer_title"] == offer.offer_title
    assert "offer_title" in serialized_data
    assert serialized_data["discount_size"] == offer.discount_size
    assert "end_date" in serialized_data
    assert serialized_data["end_date"] == offer.end_date.isoformat()

def test_offer_schema_deserialization(valid_offer_data):
    """Тестирование десериализации правильных данных."""
    schema = OfferSchema()
    deserialized_data = schema.load(valid_offer_data)

    assert isinstance(deserialized_data, SpecialOffer)
    assert deserialized_data.offer_title == valid_offer_data["offer_title"]
    assert deserialized_data.discount_size == valid_offer_data["discount_size"]

def test_offer_schema_required_fields():
    """Тестирование обязательных полей."""
    schema = OfferSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "discount_size": 10.5,
            "end_date": date.today()
        })
    assert "offer_title" in exc_info.value.messages

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "Discount Offer",
            "end_date": date.today()
        })
    assert "discount_size" in exc_info.value.messages

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "Discount Offer",
            "discount_size": 10.5
        })
    assert "end_date" in exc_info.value.messages

def test_offer_schema_validate_title():
    """Тестирование валидации поля offer_title."""
    schema = OfferSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "",
            "discount_size": 10.5,
            "end_date": date.today()
        })
    assert "Название скидки не должно быть пустым" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "A" * 51,
            "discount_size": 10.5,
            "end_date": date.today()
        })
    assert "Название скидки должно содержать не более 50 символов" in str(exc_info.value)

def test_offer_schema_validate_discount_size():
    """Тестирование валидации поля discount_size."""
    schema = OfferSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "Discount Offer",
            "discount_size": "invalid_value",
            "end_date": date.today()
        })
    assert "Размер скидки должен быть корректным числом" in str(exc_info.value)

def test_offer_schema_validate_end_date():
    """Тестирование валидации поля end_date."""
    schema = OfferSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "Discount Offer",
            "discount_size": 10,
            "end_date": None
        })
    assert "Дата окончания скидки обязательна для заполнения" in str(exc_info.value)

def test_offer_schema_empty_fields():
    """Тестирование обработки пустых обязательных полей."""
    schema = OfferSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "offer_title": "",
            "discount_size": "",
            "end_date": ""
        })
    assert "offer_title" in exc_info.value.messages
    assert "discount_size" in exc_info.value.messages
    assert "end_date" in exc_info.value.messages
