import codecs
import csv
import io
import zipfile
import re

from PIL import UnidentifiedImageError

from django.db import transaction


class CsvImportError(Exception):
    pass


class ConfigCsvImportError(CsvImportError):
    pass


class HeaderCsvImportError(CsvImportError):
    pass


class RowCsvImportError(CsvImportError):
    pass


class CsvColumnBase(object):
    DT_TEXT, DT_NUMBER, DT_MARKDOWN = range(1, 4)

    def __init__(
        self,
        name,
        field_name,
        data_type=DT_TEXT,
        required=False,
        default=None,
    ):
        self.name = name
        self.field_name = field_name
        self.data_type = data_type
        self.required = required
        self.default = default

    def is_valid(self, value):
        if self.required and not (value and value.strip()):
            return False, 'Value is required.'
        return True, ''

    def convert_value(self, value):
        if self.data_type == self.DT_NUMBER:
            converted = int(value)
        elif self.data_type == self.DT_MARKDOWN:
            raise NotImplementedError('Markdown support is not implemented yet.')
        else:
            converted = value
        return converted


class CsvColumn(CsvColumnBase):
    """
    Standard csv column mapped to single model instance field value.
    """


class CsvCustomColumn(CsvColumnBase):
    """
    This column values are not directly saved as model field values.
    """


class CsvRelatedColumn(CsvColumnBase):
    """
    Saves value in related model instance.
    """

    def __init__(
        self,
        name,
        field_name,
        related_model,
        fk_name,
        data_type=CsvColumn.DT_TEXT,
        required=False,
        default=None,
        many=True,
        separator=';',
        related_data=None
    ):
        super().__init__(
            name=name,
            field_name=field_name,
            data_type=data_type,
            required=required,
            default=default
        )
        self.related_model = related_model
        self.fk_name = fk_name
        self.many = many
        self.separator = separator
        self.related_data = related_data or {}

    def convert_values(self, values_str):
        """
        Always returns list of values, even if empty or with single element.
        """
        if not values_str.strip():
            return []
        if self.many:
            values_list = values_str.split(self.separator)
        else:
            values_list = [values_str]
        return [self.convert_value(v) for v in values_list]


class CsvImporter(object):
    model = None
    columns = []
    key_column_name = None

    def __init__(self):
        self.header = None

    @classmethod
    def get_column_by_name(cls, name):
        for column in cls.columns:
            if column.name.lower() == name.lower():
                return column
        return None

    def process_header(self, header_row):
        """
        Setting self.header to contain corresponding columns if definition is found
        or otherwise the value of the column as string from csv file.
        """
        self.header = []
        for i, name in enumerate(header_row):
            self.header.append(self.get_column_by_name(name) or name)

        # checking if all required columns are present in csv file
        for column in self.columns:
            if column.required and column not in self.header:
                raise HeaderCsvImportError(f'Required column "{column.name}" missing in csv header row.')

    def clean_row(self, row_index, row):
        """
        Try to validate values existing in the row, if corresponding column is defined.
        Otherwise ignore the value.
        """
        cleaned_data = {}
        related_list = []

        for i, value in enumerate(row):
            if i < len(self.header):
                column = self.header[i]

                if isinstance(column, CsvColumnBase):
                    is_valid, error = column.is_valid(value)
                    if not is_valid:
                        raise RowCsvImportError(
                            f'Row {row_index} has invalid value "{value}" in column {i} "{self.header[i].name}". '
                            f'Error: {error}'
                        )

                if isinstance(column, CsvColumn):
                    cleaned_data[column.field_name] = column.convert_value(value)

                elif isinstance(column, CsvRelatedColumn):
                    for val in column.convert_values(value):
                        data = column.related_data.copy()
                        data[column.field_name] = val
                        related_list.append({
                            'model': column.related_model,
                            'fk_name': column.fk_name,
                            'data': data
                        })

        return cleaned_data, related_list

    def process_row(self, row_index, row, override_existing=False):
        cleaned_data, related_list = self.clean_row(row_index, row)

        # Trying to get existing instance
        if self.key_column_name:
            key_column = self.get_column_by_name(self.key_column_name)
            try:
                instance = self.model.objects.get(
                    **{key_column.field_name: cleaned_data[key_column.field_name]}
                )
            except self.model.DoesNotExist:
                instance = None
        else:
            instance = None

        if instance:
            # Instance already present in database
            if override_existing:
                for name, value in cleaned_data.items():
                    setattr(instance, name, value)

                # Removing existing related data
                for column in self.columns:
                    if isinstance(column, CsvRelatedColumn):
                        related_instances = column.related_model.objects.filter(**{column.fk_name: instance})
                        related_instances.delete()

            else:
                raise RowCsvImportError(
                    f'Institution with {key_column.field_name} "{cleaned_data[key_column.field_name]}" '
                    'already exists.'
                )

        else:
            # New instance has to be created
            instance = self.model(**cleaned_data)

        instance.save()

        related_instances = []
        for item in related_list:
            related_obj = item['model'](
                **{item['fk_name']: instance},
                **item['data']
            )
            related_obj.save()
            related_instances.append(related_obj)

        return instance, related_instances

    def import_data(self, csv_file, override_existing=False):
        if override_existing and not self.key_column_name:
            raise ConfigCsvImportError(
                'The override_existing option is set but no key_column_name is defined in CsvImporter derived class.'
            )

        csv_file.seek(0)
        reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))

        header_row = next(reader, None)
        self.process_header(header_row)

        instances = []
        with transaction.atomic():
            for row_index, row in enumerate(reader, start=1):

                instance, related_instances = self.process_row(row_index, row, override_existing)
                instances.append({
                    'instance': instance,
                    'related_instances': related_instances
                })

        return instances


class ZipImporter(object):
    """
    Tries to save files from zip_file archive to corresponding model instances when name of the file matches
    query_fname field value of the model instance.
    """

    def __init__(self, model, file_fname, query_fname, case_sensitive=False, allowed_ext=None):
        self.model = model
        self.file_fname = file_fname
        self.query_fname = query_fname
        self.case_sensitive = case_sensitive

        if isinstance(allowed_ext, str):
            allowed_ext = [allowed_ext]
        assert isinstance(allowed_ext, (list, tuple))
        self.allowed_ext = allowed_ext

    def import_data(self, zip_file):
        imported_count = 0
        errors_list = []
        unrecog_list = []

        with zipfile.ZipFile(zip_file, 'r') as archive:

            for raw_name in archive.namelist():
                if self.allowed_ext:
                    pattern = r'\.({})$'.format('|'.join(self.allowed_ext))
                    name = re.sub(pattern, '', raw_name)

                query_params = {
                    '{n}__{i}exact'.format(n=self.query_fname, i='' if self.case_sensitive else 'i'): name
                }
                try:
                    instance = self.model.objects.get(**query_params)
                except self.model.DoesNotExist:
                    unrecog_list.append(raw_name)
                else:
                    file_content = io.BytesIO(archive.read(raw_name))
                    try:
                        getattr(instance, self.file_fname).save(name, file_content)
                    except UnidentifiedImageError:
                        errors_list.append(raw_name)
                    else:
                        imported_count += 1

        return imported_count, errors_list, unrecog_list
