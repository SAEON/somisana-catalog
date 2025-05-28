from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, edit_btn, create_btn
from somisana.const import SOMISANAScope, EntityType
from somisana.ui.admin.forms import ProductForm

bp = Blueprint(
    'product',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/')
@api.view(SOMISANAScope.PRODUCT_READ)
def index():
    all_products = api.get('/product/all_products')

    return render_template(
        'product_index.html',
        all_products=all_products,
        buttons=[
            create_btn()
        ]
    )


@bp.route('/<id>')
@api.view(SOMISANAScope.PRODUCT_READ)
def detail(id):
    product = api.get(f'/product/{id}')

    return render_template(
        'product_detail.html',
        product=product,
        entity_type=EntityType.PRODUCT.value,
        buttons=[
            edit_btn(object_id=id),
            delete_btn(object_id=id, prompt_args=(product['title'],))
        ]
    )


@bp.route('/new', methods=('GET', 'POST'))
@api.view(SOMISANAScope.PRODUCT_ADMIN)
def create():
    form = ProductForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            new_product_id = api.post(
                path='/product/',
                data=dict(
                    title=form.title.data,
                    description=form.description.data,
                    doi=form.doi.data,
                    north_bound=float(form.north_bound.data),
                    south_bound=float(form.south_bound.data),
                    east_bound=float(form.east_bound.data),
                    west_bound=float(form.west_bound.data),
                    horizontal_extent=float(form.horizontal_extent.data),
                    horizontal_resolution=float(form.horizontal_resolution.data),
                    vertical_extent=float(form.vertical_extent.data),
                    vertical_resolution=float(form.vertical_resolution.data),
                    temporal_extent=float(form.temporal_extent.data),
                    temporal_resolution=float(form.temporal_resolution.data),
                    variables=form.variables.data,
                )
            )
            flash(f'Product {new_product_id} has been created.', category='success')
            return redirect(url_for('.detail', id=new_product_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('product_edit.html', form=form)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@api.view(SOMISANAScope.PRODUCT_ADMIN)
def edit(id):
    product = api.get(f'/product/{id}')

    # Change simulation objects into array of just id's for multichecklist
    product['simulations'] = [simulation['id'] for simulation in product['simulations']]

    if request.method == 'POST':
        form = ProductForm(request.form)
    else:
        form = ProductForm(data=product)

    if request.method == 'POST' and form.validate():
        try:
            api.put(
                path=f'/product/{id}',
                data=dict(
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
@api.view(SOMISANAScope.PRODUCT_ADMIN)
def delete(id):
    api.delete(f'/product/{id}')
    flash(f'Product {id} has been deleted.', category='success')
    return redirect(url_for('.index'))



