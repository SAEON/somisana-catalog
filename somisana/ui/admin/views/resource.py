from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, create_btn
from somisana.const import SOMISANAScope, EntityType
from somisana.ui.admin.forms import ResourceForm

bp = Blueprint(
    'resource',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/<entity_type>/<entity_id>/')
@api.view(SOMISANAScope.RESOURCE_READ)
def resources(
        entity_type: str,
        entity_id: int
):
    all_resources = api.get(f'/{entity_type}/{entity_id}/resources')

    entity = api.get(f'/{entity_type}/{entity_id}')

    return render_template(
        'resource_index.html',
        resources=all_resources,
        entity_id=entity_id,
        entity_title=entity['title'],
        buttons=[
            create_btn(
                endpoint_params=dict(
                    entity_type=entity_type,
                    entity_id=entity_id
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
                    resource_id=id
                )
            )
        ]
    )


@bp.route('/new/<entity_type>/<entity_id>/', methods=['GET', 'POST'])
@api.view(SOMISANAScope.RESOURCE_ADMIN)
def create(
        entity_type: str,
        entity_id: int
):
    form = ResourceForm(request.form)
    form.file.data = request.files.get('file')

    if request.method == 'POST' and form.validate():
        try:
            if form.file.data:
                new_resource_id = api.put_files(
                    path=f'/{entity_type}/{entity_id}/resource/?resource_type={form.resource_type.data}',
                    files={'file': (form.file.data.filename, form.file.data.stream)}
                )
            else:
                new_resource_id = api.post(
                    path=f'/{entity_type}/{entity_id}/resource/',
                    data={
                        'reference': form.reference.data,
                        'resource_type': form.resource_type.data,
                    }
                )

            flash(f'Resource {new_resource_id} has been created.', category='success')
            return get_post_create_redirect(entity_type, entity_id)

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('resource_edit.html', form=form, entity_type=entity_type, entity_id=entity_id)


def get_post_create_redirect(entity_type: str, entity_id: int):
    match entity_type:
        case EntityType.SIMULATION:
            return redirect(url_for('simulation.detail', id=entity_id))
        case _:
            return redirect(url_for('.resources', entity_type=entity_type, entity_id=entity_id))


@bp.route('/<resource_id>/delete', methods=('POST',))
@api.view(SOMISANAScope.RESOURCE_ADMIN)
def delete(resource_id):
    api.delete(f'/resource/{resource_id}')
    flash(f'Resource {resource_id} has been deleted.', category='success')
    return redirect(url_for('home.index'))
