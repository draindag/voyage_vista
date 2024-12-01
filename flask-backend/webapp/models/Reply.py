"""
Этот модуль определяет модель Reply для работы с вопросами и ответами в собственном разделе тура.

Здесь описаны атрибуты комментария, его связи с авторами и турами, а также
возможные вложенные ответы.
"""

import uuid

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class Reply(db.Model):
    __tablename__ = 'replies'

    reply_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reply_text = db.Column(db.Text, nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    tour_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), nullable=False)
    parent_reply_id = db.Column(UUID(as_uuid=True), db.ForeignKey('replies.reply_id'), nullable=True)

    child_replies = db.relationship('Reply', backref=db.backref('parent_reply', remote_side=[reply_id]),
                                    lazy='dynamic', cascade='all, delete-orphan')

    @property
    def replies(self):
        return self.child_replies.all()

    def __repr__(self):
        return '<Reply {}>'.format(self.reply_text)
