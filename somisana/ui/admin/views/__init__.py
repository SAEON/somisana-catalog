from flask import Flask, Blueprint, request, session


def init_app(app: Flask):
    from . import home, product, resource, dataset

    app.register_blueprint(home.bp)
    app.register_blueprint(product.bp, url_prefix='/product')
    app.register_blueprint(dataset.bp, url_prefix='/dataset')
    app.register_blueprint(resource.bp, url_prefix='/resource')

