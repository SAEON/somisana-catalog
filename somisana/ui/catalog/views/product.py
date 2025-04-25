from pathlib import Path

from flask import Blueprint, render_template

from odp.ui.base import api, cli

bp = Blueprint('product', __name__, static_folder=Path(__file__).parent.parent / 'static')


@bp.route('/<id>')
@cli.view()
@api.user()
def index(id):
    product = cli.get(f'/product/{id}')

    local_resource_base_url = f'{api.api_url}/local_resources'

    return render_template(
        'product.html',
        product=product,
        local_resource_base_url=local_resource_base_url
    )
