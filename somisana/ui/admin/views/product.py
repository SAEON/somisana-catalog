from pathlib import Path

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, edit_btn, create_btn
from somisana.ui.admin.forms import ProductForm

bp = Blueprint(
    'product',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/')
def index():
    result = requests.get('http://localhost:2020/product/all_products')
    all_products = result.json()

    return render_template(
        'product_index.html',
        all_products=all_products,
        buttons=[
            create_btn()
        ]
    )


@bp.route('/<id>')
def detail(id):
    result = requests.get(f'http://localhost:2020/product/{id}')
    result = result.json()

    return render_template(
        'product_detail.html',
        product=result,
        buttons=[
            edit_btn(object_id=id),
            delete_btn(object_id=id, prompt_args=(result['title'],))
        ]
    )


@bp.route('/new', methods=('GET', 'POST'))
def create():
    form = ProductForm(request.form)
    populate_simulation_choices(form.simulations)

    if request.method == 'POST' and form.validate():
        try:
            response = requests.post(
                url='http://localhost:2020/product/',
                json=dict(
                    title=form.title.data,
                    description=form.description.data,
                    doi=form.doi.data,
                    north_bound=float(form.north_bound.data),
                    south_bound=float(form.south_bound.data),
                    east_bound=float(form.east_bound.data),
                    west_bound=float(form.west_bound.data),
                    simulation_ids=[int(simulation_id) for simulation_id in form.simulations.data],
                )
            )
            new_product_id = response.json()
            flash(f'Product {new_product_id} has been created.', category='success')
            return redirect(url_for('.detail', id=new_product_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('product_edit.html', form=form)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    result = requests.get(f'http://localhost:2020/product/{id}')
    product = result.json()

    # Change simulation objects into array of just id's for multichecklist
    product['simulations'] = [simulation['id'] for simulation in product['simulations']]

    if request.method == 'POST':
        form = ProductForm(request.form)
    else:
        form = ProductForm(data=product)

    populate_simulation_choices(form.simulations)

    if request.method == 'POST' and form.validate():
        try:
            requests.put(
                url=f'http://localhost:2020/product/{id}',
                json=dict(
                    title=form.title.data,
                    description=form.description.data,
                    doi=form.doi.data,
                    north_bound=float(form.north_bound.data),
                    south_bound=float(form.south_bound.data),
                    east_bound=float(form.east_bound.data),
                    west_bound=float(form.west_bound.data),
                    simulation_ids=[int(simulation_id) for simulation_id in form.simulations.data],
                )
            )
            flash(f'Product {id} has been updated.', category='success')
            return redirect(url_for('.detail', id=id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('product_edit.html', product=product, form=form)


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    requests.delete(f'http://localhost:2020/product/{id}')
    flash(f'Product {id} has been deleted.', category='success')
    return redirect(url_for('.index'))


def populate_simulation_choices(field):
    simulations = requests.get('http://localhost:2020/simulation/all').json()
    field.choices = [
        (simulation['id'], simulation['title'])
        for simulation in simulations
    ]


