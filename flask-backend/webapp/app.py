import os

from flask import Flask


def create_app(config: dict = None):
    app = Flask("voyage_vista")
    app.config.from_mapping(

    )

    return app
