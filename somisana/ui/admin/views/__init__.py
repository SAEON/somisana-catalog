from flask import Flask, Blueprint, request, session


def init_app(app: Flask):
    from . import home, product, simulation, resource

    app.register_blueprint(home.bp)
    app.register_blueprint(product.bp, url_prefix='/product')
    app.register_blueprint(simulation.bp, url_prefix='/simulation')
    app.register_blueprint(resource.bp, url_prefix='/resource')

