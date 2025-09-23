from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, create_btn, edit_btn
from somisana.const import SOMISANAScope, EntityType, ResourceType, ResourceReferenceType
from somisana.ui.admin.forms import ResourceForm, image_and_gif_files_allowed

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
            edit_btn(object_id=id),
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
    resource_type = request.args.get('resource_type')
    form = ResourceForm(request.form)
    form.file.data = request.files.get('file')
    set_form_options(form, resource_type)

    if request.method == 'POST' and form.validate():
        try:
            if form.file.data:
                new_resource_id = api.put_files(
                    path=f'/{entity_type}/{entity_id}/resource/?resource_type={form.resource_type.data}&title={form.title.data}',
                    files={'file': (form.file.data.filename, form.file.data.stream)}
                )
            else:
                new_resource_id = api.post(
                    path=f'/{entity_type}/{entity_id}/resource/',
                    data={
                        'title': form.title.data,
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


@bp.route('<id>/edit/', methods=('GET', 'POST'))
@api.view(SOMISANAScope.RESOURCE_ADMIN)
def edit(
        id: int
):
    resource = api.get(f'/resource/{id}')

    if request.method == 'POST':
        form = ResourceForm(request.form)
        form.file.data = request.files.get('file')

        if resource['reference_type'] == ResourceReferenceType.PATH.value and form.file.data:
            form.reference.data = None
        elif resource['reference_type'] == ResourceReferenceType.LINK.value:
            form.reference.data = resource['reference']

        resource_type = form.resource_type.data
    else:
        form = ResourceForm(data=resource)

        if resource['reference_type'] == 'path':
            form.reference.render_kw = {'disabled': 'disabled'}
            form.file.data = {'filename': resource['reference']}

        resource_type = resource['resource_type']

    set_form_options(form, resource_type)

    if request.method == 'POST' and form.validate():
        try:
            if form.file.data:
                api.put_files(
                    path=f'/resource/{id}/?resource_type={form.resource_type.data}&title={form.title.data}',
                    files={'file': (form.file.data.filename, form.file.data.stream)}
                )
            else:
                api.post(
                    path=f'/resource/{id}/',
                    data={
                        'title': form.title.data,
                        'reference': form.reference.data,
                        'resource_type': form.resource_type.data,
                    }
                )
            flash(f'Resource {id} has been updated.', category='success')
            return redirect(url_for('.detail', id=id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('resource_edit.html', resource=resource, form=form)


def get_post_create_redirect(entity_type: str, entity_id: int):
    match entity_type:
        case EntityType.DATASET:
            return redirect(url_for('dataset.detail', id=entity_id))
        case _:
            return redirect(url_for('.resources', entity_type=entity_type, entity_id=entity_id))


@bp.route('/<resource_id>/delete', methods=('POST',))
@api.view(SOMISANAScope.RESOURCE_ADMIN)
def delete(resource_id):
    api.delete(f'/resource/{resource_id}')
    flash(f'Resource {resource_id} has been deleted.', category='success')
    return redirect(url_for('home.index'))


def set_form_options(form, resource_type):
    match resource_type:
        case ResourceType.COVER_IMAGE | ResourceType.COVER_CLIP:
            form.resource_type.choices = [
                (ResourceType.COVER_IMAGE.value, ResourceType.COVER_IMAGE.name.replace('_', ' ').title()),
                (ResourceType.COVER_CLIP.value, ResourceType.COVER_CLIP.name.replace('_', ' ').title()),
            ]
        case ResourceType.DATA_ACCESS_URL:
            del form._fields['file']
            form.resource_type.choices = [
                (ResourceType.DATA_ACCESS_URL.value, ResourceType.DATA_ACCESS_URL.name.replace('_', ' ').title())]
        case _:
            form.resource_type.choices = [(type.value, type.name.replace('_', ' ').title()) for type in ResourceType if
                                          type.value not in [ResourceType.COVER_IMAGE, ResourceType.COVER_CLIP]]
