from pathlib import Path

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from somisana.ui.admin.forms import UrlResourceForm

from somisana.const import ResourceReferenceType

bp = Blueprint(
    'resource',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/product_resources/<product_id>/')
def product_resources(product_id):
    result = requests.get(f'http://localhost:2020/product/{product_id}/resources')
    all_product_resources = result.json()

    return render_template('resource_index.html', resources=all_product_resources)


@bp.route('/new/<product_id>/', methods=['GET', 'POST'])
def create(product_id):
    form = UrlResourceForm(request.form)

    if "submit" in request.form and form.validate():
        try:
            response = requests.post(
                url='http://localhost:2020/resource/',
                json=dict(
                    product_id=product_id,
                    reference=form.url.data,
                    resource_type=form.resource_type.data,
                )
            )
            new_resource_id = response.json()
            flash(f'Resource {new_resource_id} has been created.', category='success')
            return redirect(url_for('.product_resources', product_id=product_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('resource_edit.html', form=form)

@bp.route('/<resource_id>')
def edit(resource_id):
    result = requests.get(f'http://localhost:2020/resource/{resource_id}')
    resource = result.json()

    return render_template('resource_edit.html', resource=resource)
