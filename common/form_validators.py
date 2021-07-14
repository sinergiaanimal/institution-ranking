from django.forms import ValidationError
from django.utils.translation import ugettext as _


def validate_csv_ext(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(_('Only .csv files are supported.'))
