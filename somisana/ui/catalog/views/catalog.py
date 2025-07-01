from pathlib import Path

from flask import Blueprint, render_template

from odp.ui.base import api, cli

from somisana.config import somisana_config

bp = Blueprint('catalog', __name__, static_folder=Path(__file__).parent.parent / 'static')


@bp.route('/')
@cli.view()
@api.user()
def index():
    products = cli.get('/product/catalog_products')

    thumbnail_base_url = f'{somisana_config.SOMISANA.API_EXTERNAL_URL}/local_resources'

    return render_template('catalog.html', products=products, thumbnail_base_url=thumbnail_base_url)
