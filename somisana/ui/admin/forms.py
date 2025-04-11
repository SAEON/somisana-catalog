from wtforms import FloatField, SelectField, StringField, URLField, FileField, TextAreaField
from wtforms.validators import data_required, url, optional

from odp.ui.base.forms import BaseForm
from odp.ui.base.forms.fields import MultiCheckboxField
from somisana.const import ResourceType


class ProductForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    description = TextAreaField(label='Description', validators=[data_required()])
    doi = StringField(label='DOI')
    north_bound = FloatField(label='North Bound', validators=[data_required()])
    south_bound = FloatField(label='South Bound', validators=[data_required()])
    east_bound = FloatField(label='East Bound', validators=[data_required()])
    west_bound = FloatField(label='West Bound', validators=[data_required()])
    simulations = MultiCheckboxField(label='Simulations')


class ResourceForm(BaseForm):
    reference = URLField("Resource URL", validators=[optional(), url()])
    file = FileField("Upload File", validators=[optional()])
    resource_type = SelectField(
        "Resource Type",
        choices=[(type.value, type.name.replace('_', ' ').title()) for type in ResourceType]
    )

    def validate(self):
        if not super().validate():
            return False

        has_reference = bool(self.reference.data and self.reference.data.strip())
        has_file = bool(self.file.data and hasattr(self.file.data, 'filename') and self.file.data.filename)

        if has_reference and has_file:
            msg = "Please provide either a URL or a file, not both."
            self.reference.errors.append(msg)
            self.file.errors.append(msg)
            return False

        if not has_reference and not has_file:
            msg = "You must provide either a URL or upload a file."
            self.reference.errors.append(msg)
            self.file.errors.append(msg)
            return False

        return True


class SimulationForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    folder_path = StringField(label='Folder Path', validators=[data_required()])
    data_access_url = StringField(label='Data Access URL', validators=[optional()])