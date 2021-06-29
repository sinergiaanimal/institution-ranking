from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.managers import ActivableModelQuerySet


class TimestampedModel(models.Model):
    """
    Adds automatic creation and modification timestamp fields.
    """
    creation_timestamp = models.DateTimeField(_('Creation time stamp'), auto_now_add=True)
    modification_timestamp = models.DateTimeField(_('Modification time stamp'), auto_now=True)

    class Meta:
        abstract = True


class ActivableModel(models.Model):
    """
    Adds "is_active" field to the model and "active" method to default manager.
    """
    is_active = models.BooleanField(_('is active'), default=True)

    objects = ActivableModelQuerySet.as_manager()

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """
    Adds "order" field to the model and set it's value as the last at save if not explicitly given.
    """
    order = models.IntegerField(_('Order'), null=False, blank=True)

    class Meta:
        abstract = True

    def get_order(self):
        max_order = self.model_class().objects.aggregate(models.Max('order'))['order__max'] or 0
        return max_order + 1

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.get_order()
        super().save(*args, **kwargs)

