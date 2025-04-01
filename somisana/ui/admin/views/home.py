from pathlib import Path
import requests

from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint(
    'home',
    __name__,
    static_folder=Path(__file__).parent.parent.parent / 'catalog/static',
    static_url_path='/catalog/static'
)


@bp.route('/')
def index():
    return render_template('home.html')
