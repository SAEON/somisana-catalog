from pathlib import Path
import requests

from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint('catalog', __name__, static_folder=Path(__file__).parent.parent / 'static')


@bp.route('/')
def index():
    result = requests.get('http://localhost:2020/product/all_products')
    result = result.json()

    return result

