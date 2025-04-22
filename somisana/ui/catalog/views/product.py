from pathlib import Path

from flask import Blueprint, render_template
from somisana.const import ResourceType
from odp.ui.base import api, cli

bp = Blueprint('product', __name__, static_folder=Path(__file__).parent.parent / 'static')


@bp.route('/<id>')
@cli.view()
@api.user()
def index(id):
    product = cli.get(f'/product/{id}')

    # product_thumbnail = cli.get(f'/product/{id}/{}')

    return render_template('product.html', product=product)
