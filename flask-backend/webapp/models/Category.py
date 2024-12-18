"""
Этот модуль определяет модель Category для работы с категориями туров.

Здесь описаны атрибуты категории, ее отношения к турам и способ получения
URL для изображения категории.
"""

import os
import uuid

from sqlalchemy.dialects.postgresql import UUID
from webapp import db

file_ext = os.getenv("COVER_IMAGES_EXT")


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    category_description = db.Column(db.Text, nullable=False)
    tours = db.relationship('Tour', backref='category', lazy='dynamic',
                            cascade='all, delete-orphan')

    @property
    def category_image(self):
        return f"{self.category_id}{file_ext}"

    def __repr__(self):
        return f"<Category(name={self.category_title}, description={self.category_description})>"
