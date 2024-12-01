"""
Модуль для инициализации компонентов Flask-приложения.

Этот файл содержит инициализацию базы данных, миграций,
JWT аутентификации, Marshmallow для сереализации,
Swagger для документирования API и UploadSet для работы с изображениями.
"""

from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
swagger = Swagger()
photos = UploadSet('photos', IMAGES)
