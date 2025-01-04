import pytest
from marshmallow.exceptions import ValidationError
from webapp.schemas.ReplySchema import ReplySchema
from webapp.models.Reply import Reply

def test_reply_schema_serialization(reply):
    """Тестирование корректной сериализации комментария."""
    schema = ReplySchema()
    serialized_data = schema.dump(reply)

    assert "reply_text" in serialized_data
    assert serialized_data["reply_text"] == reply.reply_text
    assert "author" in serialized_data
    assert "replies" in serialized_data

def test_reply_schema_deserialization(valid_reply_data):
    """Тестирование корректной десериализации комментария."""
    schema = ReplySchema()
    deserialized_data = schema.load(valid_reply_data)

    assert isinstance(deserialized_data, Reply)
    assert deserialized_data.reply_text == valid_reply_data["reply_text"]
    assert deserialized_data.author_id == valid_reply_data["author_id"]
    assert deserialized_data.tour_id == valid_reply_data["tour_id"]

def test_reply_schema_empty_text(valid_reply_data):
    """Тестирование пустого текста комментария."""
    schema = ReplySchema()
    empty_text_data = valid_reply_data.copy()
    empty_text_data['reply_text'] = ""

    with pytest.raises(ValidationError) as exc_info:
        schema.load(empty_text_data)
    errors = exc_info.value.messages
    assert "reply_text" in errors
    assert errors["reply_text"] == ["Текст комментария не должен быть пустым"]

def test_reply_schema_invalid_author_id(valid_reply_data):
    """Тестирование некорректного UUID автора."""
    schema = ReplySchema()
    invalid_author_id_data = valid_reply_data.copy()
    invalid_author_id_data['author_id'] = "invalid-uuid"

    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_author_id_data)
    errors = exc_info.value.messages
    assert "author_id" in errors
    assert errors["author_id"] == ["Not a valid UUID."]

def test_reply_schema_invalid_tour_id(valid_reply_data):
    """Тестирование некорректного UUID тура."""
    schema = ReplySchema()
    invalid_tour_id_data = valid_reply_data.copy()
    invalid_tour_id_data['tour_id'] = "invalid-uuid"

    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_tour_id_data)
    errors = exc_info.value.messages
    assert "tour_id" in errors
    assert errors["tour_id"] == ["Not a valid UUID."]

