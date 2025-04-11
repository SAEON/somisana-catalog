from pathlib import Path
import requests

from odp.ui.base.templates import delete_btn, edit_btn, create_btn
from odp.lib.client import ODPAPIError
from odp.ui.base import api
from flask import Blueprint, flash, redirect, render_template, request, url_for
from somisana.ui.admin.forms import SimulationForm

bp = Blueprint(
    'simulation',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/')
def index():
    result = requests.get('http://localhost:2020/simulation/all')
    all_simulations = result.json()

    return render_template(
        'simulation_index.html',
        all_simulations=all_simulations,
        buttons=[
            create_btn()
        ]
    )


@bp.route('/<id>')
def detail(id):
    result = requests.get(f'http://localhost:2020/simulation/{id}')
    result = result.json()

    return render_template(
        'simulation_detail.html',
        simulation=result,
        buttons=[
            edit_btn(object_id=id),
            delete_btn(object_id=id, prompt_args=(result['title'],))
        ]
    )


@bp.route('/new', methods=('GET', 'POST'))
def create():
    form = SimulationForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            response = requests.post(
                url='http://localhost:2020/simulation/',
                json=dict(
                    title=form.title.data,
                    folder_path=form.folder_path.data,
                    data_access_url=form.data_access_url.data,
                )
            )
            new_simulation_id = response.json()
            flash(f'Product {new_simulation_id} has been created.', category='success')
            return redirect(url_for('.detail', id=new_simulation_id))

        except ODPAPIError as e:
            if response := api.handle_error(e):
                return response

    return render_template('simulation_edit.html', form=form)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    result = requests.get(f'http://localhost:2020/simulation/{id}')
    simulation = result.json()

    # separate get/post form instantiation to resolve
    if request.method == 'POST':
        form = SimulationForm(request.form)
    else:
        form = SimulationForm(data=simulation)

    if request.method == 'POST' and form.validate():
        try:
            requests.put(
                url=f'http://localhost:2020/simulation/{id}',
                json=dict(
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
def delete(id):
    requests.delete(f'http://localhost:2020/product/{id}')
    flash(f'Product {id} has been deleted.', category='success')
    return redirect(url_for('.index'))
