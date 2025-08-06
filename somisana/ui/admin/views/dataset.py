from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, create_btn, edit_btn
from somisana.const import SOMISANAScope, EntityType, ResourceType
from somisana.ui.admin.forms import DatasetForm, image_and_gif_files_allowed

bp = Blueprint(
    'dataset',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/product_datasets/<product_id>')
@api.view(SOMISANAScope.DATASET_READ)
def product_datasets(
        product_id: int
):
    all_product_datasets = api.get(f'/dataset/product_datasets/{product_id}')

    product = api.get(f'/product/{product_id}')

    return render_template(
        'dataset_index.html',
        datasets=all_product_datasets,
        product_title=product['title'],
        buttons=[
            create_btn(
                endpoint_params=dict(
                    product_id=product_id
                )
            )
        ]
    )


@bp.route('/<id>')
@api.view(SOMISANAScope.DATASET_READ)
def detail(id):
    dataset = api.get(f'/dataset/{id}')

    return render_template(
        'dataset_detail.html',
        dataset=dataset,
        entity_type=EntityType.DATASET.value,
        cover_image=dataset['cover_image'],
        data_access_urls=dataset['data_access_urls'],
        buttons=[
            edit_btn(object_id=id),
            delete_btn(object_id=id, prompt_args=(dataset['title'],))
        ]
    )


@bp.route('/new/<product_id>/', methods=['GET', 'POST'])
@api.view(SOMISANAScope.DATASET_ADMIN)
def create(
        product_id: int
):
    form = DatasetForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            new_dataset_id = api.post(
                path='/dataset/',
                data=dict(
                    product_id=product_id,
                    title=form.title.data,
                    folder_path=form.folder_path.data,
                    type=form.type.data,
                    identifier=form.identifier.data,
                )
            )
            flash(f'Dataset {new_dataset_id} has been created.', category='success')
            return redirect(url_for('.detail', id=new_dataset_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('dataset_edit.html', form=form, product_id=product_id)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@api.view(SOMISANAScope.DATASET_ADMIN)
def edit(id):
    dataset = api.get(f'/dataset/{id}')

    if request.method == 'POST':
        form = DatasetForm(request.form)
    else:
        form = DatasetForm(data=dataset)

    if request.method == 'POST' and form.validate():
        try:
            api.put(
                path=f'/dataset/{id}',
                data=dict(
                    product_id=dataset['product_id'],
                    title=form.title.data,
                    folder_path=form.folder_path.data,
                    type=form.type.data,
                    identifier=form.identifier.data,
                )
            )
            flash(f'Dataset {id} has been updated.', category='success')
            return redirect(url_for('.detail', id=id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('dataset_edit.html', dataset=dataset, product_id=dataset['product_id'], form=form)


@bp.route('/<id>/delete', methods=('POST',))
@api.view(SOMISANAScope.DATASET_ADMIN)
def delete(id):
    api.delete(f'/dataset/{id}')
    flash(f'Dataset {id} has been deleted.', category='success')
    return redirect(url_for('.index'))

