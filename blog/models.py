from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import datetime

from cms.models.fields import PlaceholderField
from autoslug.fields import AutoSlugField
from imagekit.models.fields import ImageSpecField, ProcessedImageField
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from pilkit.processors.resize import ResizeToFit

from common.models import ActivableModel, TimestampedModel


class BlogPost(TimestampedModel, ActivableModel):
    HEADER_WIDTH = 2000
    HEADER_HEIGHT = 1000
    HEADER_THUMB_WIDTH = 340
    HEADER_THUMB_HEIGHT = 300
    
    title = models.CharField(
        _('title'), max_length=100
    )
    slug = AutoSlugField(
        _('slug'), editable=True, populate_from='title',
        unique=True, blank=True,
        help_text=_(
            'This value is auto generated when omitted. '
            'It will represent post name in the internet address '
            '(should consist only of letters, numbers, hyphens and '
            'have to be unique).'
        )
    )
    publication_date = models.DateField(
        _('publication date'), default=datetime.today
    )
    reading_time = models.PositiveIntegerField(
        _('reading time'), null=True, blank=True,
        help_text=_('Estimated averange reading time in minutes.')
    )
    description = MarkdownField(
        _('Description'), null=False, blank=True,
        rendered_field='descr_rendered', validator=VALIDATOR_STANDARD
    )
    descr_rendered = RenderedMarkdownField(
        null=False, blank=True
    )
    header_image = ProcessedImageField(
        verbose_name=_('header image'),
        upload_to='common/blog_post/header_image',
        null=True, blank=True,
        processors=[ResizeToFit(HEADER_WIDTH, HEADER_HEIGHT, upscale=False)]
    )
    header_thumb = ImageSpecField(
        source='header_image',
        processors=[
            ResizeToFit(HEADER_THUMB_WIDTH, HEADER_THUMB_HEIGHT, upscale=False)
        ],
        format='JPEG'
    )
    header_darken = models.PositiveSmallIntegerField(
        _('header darkening'), validators=[MaxValueValidator(100)], default=50,
        help_text=_(
            'Percentage value of the darkness overlay applied '
            'to the header background image.'
        )

    )
    content_placeholder = PlaceholderField(
        verbose_name=_('CMS placeholder'),
        slotname='post_content'
    )
