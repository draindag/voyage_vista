from webapp import db
from sqlalchemy.dialects.postgresql import UUID


transactions = db.Table('transactions',
    db.Column('tour_id', UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), primary_key=True),
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key=True)
)
