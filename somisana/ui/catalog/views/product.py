from pathlib import Path

from flask import Blueprint, render_template

from odp.ui.base import api, cli

from somisana.config import somisana_config

bp = Blueprint('product', __name__, static_folder=Path(__file__).parent.parent / 'static')


@bp.route('/<id>')
@cli.view()
@api.user()
def index(id):
    product = cli.get(f'/product/{id}')

    local_resource_base_url = f'{somisana_config.SOMISANA.API_EXTERNAL_URL}/local_resources'

    superseded_by_product = {}
    if product['superseded_by_product_id']:
        superseded_by_product = cli.get(f"/product/{product['superseded_by_product_id']}")

    superseded_product = {}
    if product['superseded_product_id']:
        superseded_product = cli.get(f"/product/{product['superseded_product_id']}")

    return render_template(
        'product.html',
        product=product,
        superseded_by_product=superseded_by_product,
        superseded_product=superseded_product,
        local_resource_base_url=local_resource_base_url
    )
