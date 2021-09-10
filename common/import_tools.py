import codecs
import csv
import io
import zipfile
import re
import markdown

from PIL import UnidentifiedImageError

from django.db import transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class CsvImportError(Exception):
    pass


class ConfigCsvImportError(CsvImportError):
    pass


class HeaderCsvImportError(CsvImportError):
    pass


class RowCsvImportError(CsvImportError):
    pass


class CsvColumnBase(object):
    DT_TEXT, DT_NUMBER, DT_LINK, DT_MARKDOWN = range(1, 5)

    def __init__(
        self,
        name,
        data_type=DT_TEXT,
        required=False,
        default=None,
        priority=5,
        save_globally=False,
        do_assign=True
    ):
        """
        :param name: [str] name of the csv column
        :param data_type: [DT_*] type of the value in CSV file
        :param required: [bool] is value required?
        :param default: [any] use this value if not found in CSV file
        :param priority: [int] priority of processing, lower values have higher priority
        :param save_globally: [bool] value will be saved at assign_data stage to global_data dict
        """
        self.name = name
        self.data_type = data_type
        self.required = required
        self.default = default
        self.url_validator = URLValidator() if data_type == self.DT_LINK else None
        self.priority = priority
        self.save_globally = save_globally
        self.do_assign = do_assign

    def is_valid(self, value):
        if self.required and not (value and value.strip()):
            return False, 'Value is required.'
        if self.data_type == self.DT_LINK:
            pass  # URL validation is to strict.
            # try:
            #     self.url_validator(value)
            # except ValidationError as e:
            #     return False, e.message

        return True, ''

    def process_value(self, raw_value):
        """
        Cleans raw value according to specified data_type
        :param raw_value: value to be processed
        :return: processed value
        """
        value = raw_value.strip() if isinstance(raw_value, str) else raw_value

        if self.data_type == self.DT_NUMBER:
            value = int(value)
        elif self.data_type == self.DT_LINK:
            if not (
                value.startswith('http://') or value.startswith('https://')
            ):
                value = f'https://{value}'

        elif self.data_type == self.DT_MARKDOWN:
            value = markdown.markdown(value)

        return value

    def assign_data(self, value, instance, global_data):
        """
        Performs assigning cleaned value to the model instance.
        Should be defined in derived class.
        :param value: cleaned value
        :param instance: model instance
        :param global_data: global data dict to be used for additional processing if needed
        :return: None
        """
        raise NotImplementedError('This method should be implemented in derived class.')


class CsvFieldColumn(CsvColumnBase):
    """
    Standard csv column mapped to single model instance field value.
    """

    def __init__(
        self,
        *args,
        field_name,
        save_obj=False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.field_name = field_name
        self.save_obj = save_obj

    @staticmethod
    def get_obj(instance, field_name):
        """
        Usable when field_name is set with "instance__related_instance" format
        to get related instance object.
        """
        field_parts = '__'.split(field_name)
        obj = instance
        if len(field_parts) > 1:
            for part in field_parts[-1:]:
                obj = getattr(obj, part)
        return obj

    def assign_data(self, value, instance, global_data):
        if self.do_assign or self.save_obj:
            obj = self.get_obj(instance, self.field_name)

            if self.do_assign:
                setattr(obj, self.field_name.split('__')[-1], value)

            if self.save_obj:
                obj.save()

        if self.save_globally:
            global_data[self.name] = value


class CsvFKColumn(CsvColumnBase):
    """
    This column sets foreign key to related model based on the value.
    """

    def __init__(
        self,
        *args,
        field_name,
        related_model,
        key_field_name,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.field_name = field_name
        self.related_model = related_model
        self.key_field_name = key_field_name

    def assign_data(self, value, instance, global_data):
        try:
            related = self.related_model.objects.get(**{self.key_field_name: value})
        except self.related_model.DoesNotExist:
            raise RowCsvImportError(
                f'{self.related_model.__name__} instance with {self.key_field_name} "{value}" does not exist.'
            )
        except self.related_model.MultipleObjectsReturned:
            raise RowCsvImportError(
                f'More than one {self.related_model.__name__} instance '
                f'with {self.key_field_name} "{value}" has been found.'
            )
        if self.do_assign:
            setattr(instance, self.field_name, related)

        if self.save_globally:
            global_data[self.name] = related


class CsvRelatedColumn(CsvColumnBase):
    """
    Saves value in related model instance.
    """

    def __init__(
        self,
        *args,
        field_name,
        related_model,
        fk_name,
        priority=6,
        many=True,
        separator=';',
        related_data=None,
        **kwargs
    ):
        super().__init__(*args, priority=priority, **kwargs)
        self.field_name = field_name
        self.related_model = related_model
        self.fk_name = fk_name
        self.many = many
        self.separator = separator
        self.related_data = related_data or {}

    def process_value(self, value):
        """
        Always returns list of values, even if empty or with single element.
        """
        value = super().process_value(value)
        if not value:
            return []
        if self.many:
            values_list = value.split(self.separator)
        else:
            values_list = [value]

        processed_list = []
        for val in values_list:
            data = self.related_data.copy()
            data[self.field_name] = super().process_value(val)
            processed_list.append({
                'model': self.related_model,
                'fk_name': self.fk_name,
                'data': data
            })
        return processed_list

    def assign_data(self, value, instance, global_data, remove_existing=True):
        """
        :param value: [list] list of processed values
        :param instance: [Model] model instance
        :param remove_existing: [bool] should existing data be removed before assigning current data?
        :param global_data: [dict] global data dict injected by importer
        :return:
        """
        # Removing existing related data
        if remove_existing:
            related_instances = self.related_model.objects.filter(**{self.fk_name: instance})
            related_instances.delete()

        related_objs = []
        for item in value:
            related_obj = item['model'](
                **{item['fk_name']: instance},
                **item['data']
            )
            related_obj.save()
            related_objs.append(related_obj)

        if self.save_globally:
            global_data[self.name] = related_objs


class CsvImporter(object):
    model = None
    columns = []
    key_column_name = None
    processors = {}
    save_instance_at_priority = [5]  # instance will be saved after processing columns with this priority

    def __init__(self):
        self.header = None
        self.global_data = {}

    @classmethod
    def get_column_by_name(cls, name):
        for column in cls.columns:
            if column.name.lower() == name.lower():
                return column
        return None

    def pre_import(self, override_existing=False):
        """
        Override this method to perform any pre import operations.
        """
        pass

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
        Tries to validate values existing in the row, if corresponding column is defined.
        Otherwise ignore the value.
        """
        cleaned_data = {}

        for i, value in enumerate(row):
            if i < len(self.header):
                column = self.header[i]

                if isinstance(column, CsvColumnBase):
                    is_valid, error = column.is_valid(value)
                    if not is_valid:
                        raise RowCsvImportError(
                            f'Row {row_index + 1} has invalid value "{value}" in column {i} "{self.header[i].name}". '
                            f'Error: {error}'
                        )

                    cleaned_data[column.name] = column.process_value(value)

        return cleaned_data

    def process_row(self, row_index, row, override_existing=False):
        """
        Performs data assign for single CSV row.
        :param row_index: [int] number of the row in CSV file
        :param row: [list] row data read from CSV file
        :param override_existing: [bool] should existing model instances be overridden?
            works only when key_column_name is set on CsvImporter derived class
        :return: [Model] updated model instance
        """
        cleaned_data = self.clean_row(row_index, row)

        # Trying to get existing instance
        if self.key_column_name and self.key_column_name != 'dummy':
            key_column = self.get_column_by_name(self.key_column_name)
            try:
                instance = self.model.objects.get(
                    **{key_column.field_name: cleaned_data[key_column.name]}
                )
            except self.model.DoesNotExist:
                instance = None
        else:
            key_column = None
            instance = None

        if instance:
            # Instance already present in database
            if not override_existing:
                raise RowCsvImportError(
                    f'Institution with {key_column.field_name} "{cleaned_data[key_column.name]}" '
                    'already exists.'
                )
        else:
            # New instance has to be created
            instance = self.model()

        priorities = {}
        for column in self.columns:
            if column.priority not in priorities:
                priorities[column.priority] = []
            priorities[column.priority].append(column)

        priorities = dict(sorted(priorities.items()))

        for priority, columns in priorities.items():
            for column in columns:
                column.assign_data(cleaned_data[column.name], instance, self.global_data)

            if priority in self.processors:
                for processor_fn in self.processors[priority]:
                    processor_fn(instance, self.global_data)

            if priority in self.save_instance_at_priority:
                instance.save()

        return instance

    def import_data(self, csv_file, override_existing=False, delimiter=';'):
        """
        Main method called to perform import operation.
        :param csv_file: opened CSV file containing data to be imported
        :param override_existing: [bool] should existing records be overridden?
        :return: [list of Model] list of updated instances
        """
        if override_existing and not self.key_column_name:
            raise ConfigCsvImportError(
                'The override_existing option is set but no key_column_name '
                'is defined in CsvImporter derived class.'
            )

        csv_file.seek(0)
        reader = csv.reader(
            codecs.iterdecode(csv_file, 'utf-8-sig'), delimiter=delimiter
        )

        header_row = next(reader, None)
        self.process_header(header_row)

        instances = []
        with transaction.atomic():
            self.pre_import(override_existing=override_existing)
            for row_index, row in enumerate(reader, start=1):

                instance = self.process_row(row_index, row, override_existing)
                instances.append(instance)

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
