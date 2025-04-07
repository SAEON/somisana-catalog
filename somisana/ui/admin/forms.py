from wtforms import FloatField, SelectField, StringField, FormField, FieldList, URLField, SubmitField
from wtforms.validators import data_required, url

from odp.ui.base.forms import BaseForm
from odp.ui.base.forms.fields import MultiCheckboxField
from somisana.const import ResourceType


class UrlResourceForm(BaseForm):
    url = URLField("Resource URL", validators=[data_required(), url()])
    resource_type = SelectField(
        "Resource Type",
        choices=[(type.value, type.name.replace('_', ' ').title()) for type in ResourceType]
    )


class ProductForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    description = StringField(label='Description', validators=[data_required()])
    doi = StringField(label='DOI')
    north_bound = FloatField(label='North Bound', validators=[data_required()])
    south_bound = FloatField(label='South Bound', validators=[data_required()])
    east_bound = FloatField(label='East Bound', validators=[data_required()])
    west_bound = FloatField(label='West Bound', validators=[data_required()])
    simulations = MultiCheckboxField(label='Simulations')
