import pytest

from marshmallow import ValidationError

from webapp.schemas.TourSchema import TourSchema
from webapp.models.Tour import Tour

def test_tour_schema_serialization(tour):
    """Тест успешной сериализации тура с предложением."""
    schema = TourSchema()

    serialized_data = schema.dump(tour)

    assert "tour_title" in serialized_data
    assert serialized_data["tour_title"] == tour.tour_title
    assert "tour_description" in serialized_data
    assert serialized_data["tour_description"] == tour.tour_description
    assert "tour_price" in serialized_data
    assert str(serialized_data["tour_price"]) == str(tour.tour_price)
    assert "price_with_discount" in serialized_data
    assert len(serialized_data["offers"]) == 0

def test_tour_schema_deserialization_valid_data(valid_tour_data):
    """Тест десериализации правильных данных."""
    schema = TourSchema()

    deserialized_data = schema.load(valid_tour_data)

    assert isinstance(deserialized_data, Tour)
    assert deserialized_data.tour_title == valid_tour_data["tour_title"]
    assert deserialized_data.tour_text == valid_tour_data["tour_text"]
    assert deserialized_data.tour_description == valid_tour_data["tour_description"]
    assert deserialized_data.tour_price == valid_tour_data["tour_price"]

def test_tour_schema_empty_title(valid_tour_data):
    """Тестирование пустого названия тура."""
    schema = TourSchema()
    empty_title_data = valid_tour_data.copy()
    empty_title_data["tour_title"] = ""
    with pytest.raises(ValidationError) as exc_info:
        schema.load(empty_title_data)
    errors = exc_info.value.messages
    assert "tour_title" in errors
    assert errors["tour_title"] == ["Название тура не должно быть пустым"]

def test_tour_schema_long_title(valid_tour_data):
    """Тестирование слишком длинного названия тура."""
    schema = TourSchema()
    long_title_data = valid_tour_data.copy()
    long_title_data["tour_title"] = "A" * 41

    with pytest.raises(ValidationError) as exc_info:
        schema.load(long_title_data)
    errors = exc_info.value.messages
    assert "tour_title" in errors
    assert errors["tour_title"] == ["Название тура должно содержать не более 40 символов"]

def test_tour_schema_empty_description(valid_tour_data):
    """Тестирование пустого описания тура."""
    schema = TourSchema()
    empty_description_data = valid_tour_data.copy()
    empty_description_data["tour_description"] = ""

    with pytest.raises(ValidationError) as exc_info:
        schema.load(empty_description_data)
    errors = exc_info.value.messages
    assert "tour_description" in errors
    assert errors["tour_description"] == ["Описание тура не должно быть пустым"]

def test_tour_schema_invalid_price(valid_tour_data):
    """Тестирование некорректной цены тура."""
    schema = TourSchema()
    invalid_price_data = valid_tour_data.copy()
    invalid_price_data["tour_price"] = -1

    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_price_data)
    errors = exc_info.value.messages
    assert "tour_price" in errors
    assert errors["tour_price"] == ["Цена тура должна быть положительным числом"]

def test_tour_schema_empty_start_date(valid_tour_data):
    """Тестирование пустой даты начала тура."""
    schema = TourSchema()
    empty_start_date_data = valid_tour_data.copy()
    empty_start_date_data["tour_start_date"] = None

    with pytest.raises(ValidationError) as exc_info:
        schema.load(empty_start_date_data)
    errors = exc_info.value.messages
    assert "tour_start_date" in errors
    assert errors["tour_start_date"] == ["Дата начала тура обязательна для заполнения"]

def test_tour_schema_empty_end_date(valid_tour_data):
    """Тестирование пустой даты окончания тура."""
    schema = TourSchema()
    empty_end_date_data = valid_tour_data.copy()
    empty_end_date_data["tour_end_date"] = None

    with pytest.raises(ValidationError) as exc_info:
        schema.load(empty_end_date_data)
    errors = exc_info.value.messages
    assert "tour_end_date" in errors
    assert errors["tour_end_date"] == ["Дата окончания тура обязательна для заполнения"]
