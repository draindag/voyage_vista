from flask_login import UserMixin
from werkzeug.security import check_password_hash

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True)
    login = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.Text, index=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def get_id(self):
        return self.user_id

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.login)
