import uuid

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_text = db.Column(db.Text, nullable=False)
    review_value = db.Column(db.Integer, nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    tour_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), nullable=False)

    def __repr__(self):
        return '<Reply {}>'.format(self.reply_text)
