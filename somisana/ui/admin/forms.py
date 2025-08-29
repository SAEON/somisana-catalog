from wtforms import FloatField, SelectField, StringField, URLField, FileField, TextAreaField, ValidationError, \
    RadioField
from wtforms.validators import data_required, url, optional

from odp.ui.base.forms import BaseForm

from somisana.const import DatasetType


class ProductForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    description = TextAreaField(label='Description', validators=[data_required()])
    doi = StringField(label='DOI')
    north_bound = FloatField(label='North Bound', validators=[data_required()])
    south_bound = FloatField(label='South Bound', validators=[data_required()])
    east_bound = FloatField(label='East Bound', validators=[data_required()])
    west_bound = FloatField(label='West Bound', validators=[data_required()])
    horizontal_resolution = StringField(label='Horizontal Resolution', validators=[optional()])
    vertical_extent = StringField(label='Vertical Extent', validators=[optional()])
    vertical_resolution = StringField(label='Vertical Resolution', validators=[optional()])
    temporal_extent = StringField(label='Temporal Extent', validators=[optional()])
    temporal_resolution = StringField(label='Temporal Resolution', validators=[optional()])
    variables = StringField(label='Variables', validators=[optional()], description='comma separated')
    superseded_product_id = RadioField(label='Supersedes', validators=[optional()],
                                       description='Product superseded by this one')


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


class DatasetForm(BaseForm):
    title = StringField(label='Title', validators=[data_required()])
    folder_path = StringField(label='Folder Path', validators=[data_required()])
    identifier = StringField(label='Identifier', validators=[data_required()],
                             description='Unique identifier used by the ingester')
    type = SelectField(label='Type', validators=[data_required()],
                       choices=[(dataset_type.value, dataset_type.name) for dataset_type in DatasetType],
                       description='Tells the ingester what type of data is being ingested')


def image_and_gif_files_allowed(form, field):
    if field.data:
        filename = field.data.filename.lower()
        if not filename.endswith(('.jpg', '.png', '.gif')):
            raise ValidationError('Only .jpg, .png, or .gif files are allowed.')
