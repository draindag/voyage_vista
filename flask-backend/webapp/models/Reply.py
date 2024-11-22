from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class Reply(db.Model):
    __tablename__ = 'replies'

    reply_id = db.Column(UUID(as_uuid=True), primary_key=True)
    reply_text = db.Column(db.Text, nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    tour_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), nullable=False)
    parent_reply_id = db.Column(UUID(as_uuid=True), db.ForeignKey('replies.reply_id'), nullable=True)
    replies = db.relationship('Reply', remote_side=[reply_id], backref='parent_reply', lazy='select',
                              cascade='all')

    def __repr__(self):
        return '<Reply {}>'.format(self.reply_text)
