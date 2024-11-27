from marshmallow import fields, post_load

from webapp import ma
from webapp.models.Reply import Reply


class ReplySchema(ma.Schema):
    reply_id = fields.UUID(dump_only=True)
    reply_text = fields.String(required=True,
                                   error_messages={"required": "Текст комментария обязателен для заполнения"})
    author_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Автор отзыва обязателен для указания",
                                                "invalid": "ID должен быть корректным UUID"})
    tour_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Тур отзыва обязателен для указания",
                                                "invalid": "ID должен быть корректным UUID"})
    parent_reply_id = fields.UUID(load_only=True, error_messages={"invalid": "ID должен быть корректным UUID"})

    author = fields.Nested("UserSchema", dump_only=True, exclude=("fav_tours","transactions", "email"))
    replies = fields.Nested("ReplySchema", dump_only=True, many=True)

    @post_load
    def create_review(self, data, **kwargs):
        return Reply(**data)