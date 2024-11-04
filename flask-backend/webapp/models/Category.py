from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True)
    category_title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    category_description = db.Column(db.Text, nullable=False)
    tours = db.relationship('Tour', backref='category', lazy='dynamic')

    def __repr__(self):
        return f"<Category(name={self.category_title}, description={self.category_description})>"

    def to_dict(self):
        return {
            'category_id': str(self.category_id),
            'category_title': self.category_title,
            'category_description': self.category_description
        }
