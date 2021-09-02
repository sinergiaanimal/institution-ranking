from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.models.fields import PlaceholderField
from djangocms_bootstrap4.fields import AttributesField, TagTypeField
from filer.fields.image import FilerImageField

from common.managers import ActivableModelQuerySet


# Abstract base models

class TimestampedModel(models.Model):
    """
    Adds automatic creation and modification timestamp fields.
    """
    creation_timestamp = models.DateTimeField(
        _('Creation time stamp'), auto_now_add=True
    )
    modification_timestamp = models.DateTimeField(
        _('Modification time stamp'), auto_now=True
    )

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
    Adds "order" field to the model and set it's value as the last at save
     if not explicitly given.
    """
    order = models.IntegerField(_('Order'), null=False, blank=True)

    class Meta:
        abstract = True
        ordering = ('order',)

    def get_order(self):
        max_order = self.__class__.objects.aggregate(
            models.Max('order')
        )['order__max'] or 0
        return max_order + 1

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.get_order()
        super().save(*args, **kwargs)


def content_placeholder_slotname(instance):
    return instance.slug


# Django CMS related models

class ContentPlaceholder(TimestampedModel):
    """
    Placeholder model to use with pages outside of CMS.
    """
    slug = models.SlugField(_('slug'), unique=True)
    placeholder = PlaceholderField(
        verbose_name=_('CMS placeholder'),
        slotname=content_placeholder_slotname
    )
    description = models.TextField(
        _('description'), null=True, blank=True,
        help_text=_('Description for administrator.')
    )

    def __str__(self):
      return self.slug


class WrapperPluginModel(CMSPlugin):
    """
    Wraps contents into simple HTML element with configurable type
     and attributes.
    """
    tag_type = TagTypeField()
    attributes = AttributesField(
        verbose_name=_('attributes'),
        blank=True,
        excluded_keys=[]
    )

    def __str__(self):
        return f'(Wrapper)'


class CoverPluginModel(CMSPlugin):
    """
    Allows to create container with full width background image.
    """
    tag_type = TagTypeField()
    image = FilerImageField(
        verbose_name=_('image'),
        null=True, blank=True, on_delete=models.CASCADE,
        related_name='cover_images'
    )
    attributes = AttributesField(
        verbose_name=_('attributes'),
        blank=True,
        excluded_keys=[]
    )
    darken = models.PositiveSmallIntegerField(
        _('darken'), validators=[MaxValueValidator(100)], default=0,
        help_text=_(
            'Percentage value of the darkness overlay applied '
            'to the background.'
        )
    )

    def __str__(self):
        return f'(Cover)'
