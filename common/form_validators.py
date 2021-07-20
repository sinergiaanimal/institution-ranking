from django.forms import ValidationError
from django.utils.translation import ugettext as _


def validate_ext(value, extensions):
    """
    :param value: file name
    :param extensions: extension as string or list of extensions
    :return: None
    """
    if isinstance(extensions, str):
        extensions = [extensions]
    for ext in extensions:
        if value.name.endswith(f'.{ext}'):
            return
    raise ValidationError(
        _('Only {extensions} files are supported.'.format(extensions=", ".join(extensions)))
    )


def validate_csv_ext(value):
    validate_ext(value, 'csv')


def validate_zip_ext(value):
    validate_ext(value, 'zip')
