from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for

from odp.lib.client import ODPAPIError
from odp.ui.base import api
from odp.ui.base.templates import delete_btn, edit_btn, create_btn
from somisana.const import SOMISANAScope, EntityType
from somisana.ui.admin.forms import SimulationForm

bp = Blueprint(
    'simulation',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/')
@api.view(SOMISANAScope.SIMULATION_READ)
def index():
    all_simulations = api.get('/simulation/all')

    return render_template(
        'simulation_index.html',
        all_simulations=all_simulations,
        buttons=[
            create_btn()
        ]
    )


@bp.route('/<id>')
@api.view(SOMISANAScope.SIMULATION_READ)
def detail(id):
    simulation = api.get(f'/simulation/{id}')

    return render_template(
        'simulation_detail.html',
        simulation=simulation,
        entity_type=EntityType.SIMULATION.value,
        cover_image=simulation['cover_image'],
        buttons=[
            edit_btn(object_id=id),
            delete_btn(object_id=id, prompt_args=(simulation['title'],))
        ]
    )


@bp.route('/new', methods=('GET', 'POST'))
@api.view(SOMISANAScope.SIMULATION_ADMIN)
def create():
    form = SimulationForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            new_simulation_id = api.post(
                path='/simulation/',
                data=dict(
                    title=form.title.data,
                    folder_path=form.folder_path.data,
                    data_access_url=form.data_access_url.data,
                )
            )
            flash(f'Product {new_simulation_id} has been created.', category='success')
            return redirect(url_for('.detail', id=new_simulation_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('simulation_edit.html', form=form)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@api.view(SOMISANAScope.SIMULATION_ADMIN)
def edit(id):
    simulation = api.get(f'/simulation/{id}')

    # separate get/post form instantiation to resolve
    if request.method == 'POST':
        form = SimulationForm(request.form)
    else:
        form = SimulationForm(data=simulation)

    if request.method == 'POST' and form.validate():
        try:
            api.put(
                path=f'/simulation/{id}',
                data=dict(
                    title=form.title.data,
                    folder_path=form.folder_path.data,
                    data_access_url=form.data_access_url.data,
                )
            )
            flash(f'Simulation {id} has been updated.', category='success')
            return redirect(url_for('.detail', id=id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('simulation_edit.html', simulation=simulation, form=form)


@bp.route('/<id>/delete', methods=('POST',))
@api.view(SOMISANAScope.SIMULATION_ADMIN)
def delete(id):
    api.delete(f'/product/{id}')
    flash(f'Product {id} has been deleted.', category='success')
    return redirect(url_for('.index'))
