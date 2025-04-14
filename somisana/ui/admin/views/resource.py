from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, create_btn
from somisana.const import SOMISANAScope
from somisana.ui.admin.forms import ResourceForm

bp = Blueprint(
    'resource',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/product_resources/<product_id>/')
@api.view(SOMISANAScope.RESOURCE_READ)
def product_resources(product_id):
    all_product_resources = api.get(f'/resource/product_resources/{product_id}')

    product = api.get(f'/product/{product_id}')

    return render_template(
        'resource_index.html',
        resources=all_product_resources,
        product_id=product_id,
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
@api.view(SOMISANAScope.RESOURCE_READ)
def detail(id):
    resource = api.get(f'/resource/{id}')

    return render_template(
        'resource_detail.html',
        resource=resource,
        buttons=[
            delete_btn(
                object_id=id,
                prompt_args=(resource['reference'],),
                endpoint_params=dict(
                    product_id=resource['product_id'],
                    resource_id=id
                )
            )
        ]
    )


@bp.route('/new/<product_id>/', methods=['GET', 'POST'])
@api.view(SOMISANAScope.RESOURCE_ADMIN)
def create(product_id):
    form = ResourceForm(request.form)
    form.file.data = request.files.get('file')

    if request.method == 'POST' and form.validate():
        try:
            if form.file.data:
                new_resource_id = api.put_files(
                    path=f'/resource/?product_id={product_id}&resource_type={form.resource_type.data}',
                    files={'file': (form.file.data.filename, form.file.data.stream)}
                )
            else:
                new_resource_id = api.post(
                    path='/resource/',
                    data={
                        'product_id': product_id,
                        'reference': form.reference.data,
                        'resource_type': form.resource_type.data,
                    }
                )

            flash(f'Resource {new_resource_id} has been created.', category='success')
            return redirect(url_for('.product_resources', product_id=product_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('resource_edit.html', form=form, product_id=product_id)


@bp.route('<product_id>/<resource_id>/delete', methods=('POST',))
@api.view(SOMISANAScope.RESOURCE_ADMIN)
def delete(product_id, resource_id):
    api.delete(f'/resource/{resource_id}')
    flash(f'Resource {resource_id} has been deleted.', category='success')
    return redirect(url_for('.product_resources', product_id=product_id))
