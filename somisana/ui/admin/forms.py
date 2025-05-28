from wtforms import FloatField, SelectField, StringField, URLField, FileField, TextAreaField, ValidationError, FieldList
from wtforms.validators import data_required, url, optional, Regexp

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
    horizontal_extent = FloatField(label='Horizontal Extent', validators=[])
    horizontal_resolution = FloatField(label='Horizontal Resolution', validators=[])
    vertical_extent = FloatField(label='Vertical Extent', validators=[])
    vertical_resolution = FloatField(label='Vertical Resolution', validators=[])
    temporal_extent = FloatField(label='Temporal Extent', validators=[])
    temporal_resolution = FloatField(label='Temporal Resolution', validators=[])
    variables = StringField(label='Variables', validators=[], description='comma separated')


class ResourceForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    reference = URLField("Resource URL", validators=[optional(), url()])
    file = FileField("Upload File", validators=[optional()])
    resource_type = SelectField("Resource Type")

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


class DatasetForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    folder_path = StringField(label='Folder Path', validators=[data_required()])


def image_and_gif_files_allowed(form, field):
    if field.data:
        filename = field.data.filename.lower()
        if not filename.endswith(('.jpg', '.png', '.gif')):
            raise ValidationError('Only .jpg, .png, or .gif files are allowed.')
