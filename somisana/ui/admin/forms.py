from odp.ui.base.forms import BaseForm

from wtforms import BooleanField, FloatField, SelectField, StringField, DateField
from wtforms.validators import optional, data_required

from odp.ui.base.forms.fields import MultiCheckboxField


class ProductForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    description = StringField(label='Description', validators=[data_required()])
    doi = StringField(label='DOI')
    north_bound = FloatField(label='North Bound', validators=[data_required()])
    south_bound = FloatField(label='South Bound', validators=[data_required()])
    east_bound = FloatField(label='East Bound', validators=[data_required()])
    west_bound = FloatField(label='West Bound', validators=[data_required()])
    simulations = MultiCheckboxField(label='Simulations')
