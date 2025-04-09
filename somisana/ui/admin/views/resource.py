from pathlib import Path

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, edit_btn
from somisana.ui.admin.forms import UrlResourceForm

bp = Blueprint(
    'resource',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/product_resources/<product_id>/')
def product_resources(product_id):
    resource_results = requests.get(f'http://localhost:2020/resource/product_resources/{product_id}')
    all_product_resources = resource_results.json()

    product_result = requests.get(f'http://localhost:2020/product/{product_id}')
    product_result = product_result.json()

    return render_template(
        'resource_index.html',
        resources=all_product_resources,
        product_id=product_id,
        product_title=product_result['title']
    )


@bp.route('/<id>')
def detail(id):
    result = requests.get(f'http://localhost:2020/resource/{id}')
    result = result.json()

    return render_template(
        'resource_detail.html',
        resource=result,
        buttons=[
            edit_btn(object_id=id),
            delete_btn(object_id=id, prompt_args=(result['reference'],))
        ]
    )


@bp.route('/new/<product_id>/', methods=['GET', 'POST'])
def create(product_id):
    form = UrlResourceForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            response = requests.post(
                url='http://localhost:2020/resource/',
                json=dict(
                    product_id=product_id,
                    reference=form.reference.data,
                    resource_type=form.resource_type.data,
                )
            )
            new_resource_id = response.json()
            flash(f'Resource {new_resource_id} has been created.', category='success')
            return redirect(url_for('.product_resources', product_id=product_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('resource_edit.html', form=form, product_id=product_id)


@bp.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    result = requests.get(f'http://localhost:2020/resource/{id}')
    resource = result.json()

    if request.method == 'POST':
        form = UrlResourceForm(request.form)
    else:
        form = UrlResourceForm(data=resource)

    if request.method == 'POST' and form.validate():
        try:
            requests.put(
                url=f'http://localhost:2020/resource/{id}',
                json=dict(
                    reference=form.reference.data,
                    product_id=resource['product_id'],
                    resource_type=form.resource_type.data,
                )
            )
            flash(f'Resource {id} has been updated.', category='success')
            return redirect(url_for('.detail', id=id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('resource_edit.html', resource=resource, form=form)


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    requests.delete(f'http://localhost:2020/resource/{id}')
    flash(f'Resource {id} has been deleted.', category='success')
    return redirect(url_for('.index'))