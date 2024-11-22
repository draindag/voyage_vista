import uuid

from sqlalchemy import CheckConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from webapp import db
from sqlalchemy.dialects.postgresql import UUID
from webapp.models.Reply import Reply
from webapp.models.Review import Review
from webapp.models.FavTour import FavTour


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.Text, index=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="visitor")
    replies = db.relationship('Reply', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    fav_tours = db.relationship('FavTour', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint("role IN ('visitor', 'moderator', 'admin')", name="users_role_check"),
    )

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def get_fav_tours(self):
        return [fav_tour.tour for fav_tour in self.fav_tours]

    def __repr__(self):
        return '<User {}>'.format(self.login)
