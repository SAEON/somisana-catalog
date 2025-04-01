from flask import Flask, Blueprint, request, session


def init_app(app: Flask):
    from . import home, catalog

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp, url_prefix='/catalog')

