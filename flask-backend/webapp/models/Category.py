import os
import uuid

from webapp import db
from sqlalchemy.dialects.postgresql import UUID

upload_folder = os.getenv("UPLOADED_PHOTOS_DEST")
file_ext = os.getenv("COVER_IMAGES_EXT")


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    category_description = db.Column(db.Text, nullable=False)
    tours = db.relationship('Tour', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def category_image(self):
        return f"{upload_folder}{self.category_id}{file_ext}"

    def __repr__(self):
        return f"<Category(name={self.category_title}, description={self.category_description})>"
