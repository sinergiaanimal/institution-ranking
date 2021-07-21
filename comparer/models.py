from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Q
from django.conf import settings

from autoslug import AutoSlugField
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

from cms.models import CMSPlugin

from common.managers import ActivableModelQuerySet
from common.models import TimestampedModel, ActivableModel, OrderedModel


__all__ = (
    'PolicyCategory', 'PolicyCriterion', 'Institution', 'SocialMediaLink', 'InstitutionEmail', 'InstitutionScore',
    'InstitutionPolicy', 'MessageTemplate', 'RankingBoxPluginModel', 'RankingBrowserPluginModel'
)


class PolicyCategory(OrderedModel, ActivableModel, TimestampedModel):
    name = models.CharField(_('name'), max_length=250)
    slug = models.SlugField(_('slug'), unique=True)
    max_score = models.PositiveIntegerField(_('max_score'), default=0)

    # criterions - defined in comparer.models.PolicyCriterion.category
    # browser_plugin_instances - defined in comparer.models.RankingBrowserPluginModel

    class Meta:
        verbose_name = _('Policy category')
        verbose_name_plural = _('Policy categories')
        ordering = ['order']

    def __str__(self):
        return self.name


class PolicyCriterion(OrderedModel, ActivableModel, TimestampedModel):
    name = models.CharField(_('name'), max_length=250)
    category = models.ForeignKey(
        verbose_name=_('category'), to=PolicyCategory, on_delete=models.CASCADE,
        related_name='criterions'
    )

    class Meta:
        verbose_name = _('Policy criterion')
        verbose_name_plural = _('Policy criterions')

    def __str__(self):
        return self.name


class InstitutionQuerySet(ActivableModelQuerySet):

    def with_scores(self):
        query_dict = {
            'score_total': models.Sum('scores__score')
        }
        for slug in settings.POLICY_CATEGORY_SLUGS:
            query_dict[f'score_{slug}'] = Sum(
                'scores__score',
                filter=Q(scores__criterion__category__slug=slug)
            )
        return self.annotate(**query_dict)


class Institution(ActivableModel, TimestampedModel):
    LOGO_WIDTH, LOGO_HEIGHT = 240, 240
    LOGO_THUMB_WIDTH, LOGO_THUMB_HEIGHT = 30, 30

    name = models.CharField(_('name'), max_length=250)
    slug = AutoSlugField(_('slug'), editable=True, populate_from='name', unique=True)
    description = models.TextField(_('description'), blank=True)
    region = models.CharField(_('region'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100)
    logo = ProcessedImageField(
        verbose_name=_('logo'),
        upload_to='comparer/institution/logo',
        null=True, blank=True,
        processors=[ResizeToFit(LOGO_WIDTH, LOGO_HEIGHT)]
    )
    logo_thumb = ImageSpecField(
        source='logo',
        processors=[ResizeToFit(LOGO_THUMB_WIDTH, LOGO_THUMB_HEIGHT)],
        format='PNG'
    )

    # social_media_links = defined in comparer.models.SocialMediaLink.institution
    # emails = defined in comparer.models.InstitutionEmail.institution
    # scores = defined in comparer.models.InstitutionScore.institution

    objects = InstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')

    def __str__(self):
        return self.name


class SocialMediaLink(ActivableModel, TimestampedModel):
    FACEBOOK, INSTAGRAM, TWITTER, LINKEDIN, YOUTUBE, WEBSITE, EMAIL, ANOTHER \
        = range(1, 9)
    KIND_CHOICES = (
        (FACEBOOK, _('Facebook')),
        (INSTAGRAM, _('Instagram')),
        (TWITTER, _('Twitter')),
        (LINKEDIN, _('LinkedIn')),
        (YOUTUBE, _('YouTube')),
        (WEBSITE, _('Website')),
        (ANOTHER, _('Another')),
    )

    institution = models.ForeignKey(
        verbose_name=_('institution'), to=Institution, on_delete=models.CASCADE,
        related_name='social_media_links'
    )
    kind = models.PositiveSmallIntegerField(_('kind'), choices=KIND_CHOICES)
    url = models.URLField(_('URL address'))

    class Meta:
        verbose_name = _('Social media link')
        verbose_name_plural = _('Social media links')

    def __str__(self):
        return self.url


class InstitutionEmail(ActivableModel, TimestampedModel):
    institution = models.ForeignKey(
        verbose_name=_('institution'), to=Institution, on_delete=models.CASCADE,
        related_name='emails'
    )
    address = models.EmailField(_('e-mail address'))

    class Meta:
        verbose_name = _('Institution e-mail')
        verbose_name_plural = _('Institution e-mails')

    def __str__(self):
        return self.address


class InstitutionScore(ActivableModel, TimestampedModel):
    institution = models.ForeignKey(
        verbose_name=_('institution'), to=Institution, on_delete=models.CASCADE,
        related_name='scores'
    )
    criterion = models.ForeignKey(
        verbose_name=_('policy criterion'), to=PolicyCriterion, on_delete=models.CASCADE,
        related_name='scores'
    )
    comment = models.TextField(_('comment'), blank=True)
    score = models.IntegerField(_('score'), default=0)

    # policies - defined in comparer.InstitutionPolicy.score

    def __str__(self):
        return self.score


class InstitutionPolicy(ActivableModel, TimestampedModel):
    score = models.ForeignKey(
        verbose_name=_('score'), to=InstitutionScore, on_delete=models.CASCADE,
        related_name='policies'
    )
    title = models.CharField(_('title'), max_length=250)
    link = models.URLField(_('link'), blank=True)
    text = models.TextField(_('text'), blank=True)

    class Meta:
        verbose_name = _('Institution policy')
        verbose_name_plural = _('Institution policies')

    def __str__(self):
        return self.title


class MessageTemplate(ActivableModel, TimestampedModel):
    GOOD, NEUTRAL, BAD = range(1, 4)
    KIND_CHOICES = (
        (GOOD, _('good')),
        (NEUTRAL, _('neutral')),
        (BAD, _('bad')),
    )

    kind = models.PositiveSmallIntegerField(_('kind'), choices=KIND_CHOICES, default=NEUTRAL)
    title = models.TextField(_('title'))
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('Message template')
        verbose_name_plural = _('Message templates')

    def __str__(self):
        return self.title


class RankingBoxPluginModel(CMSPlugin):
    title = models.CharField(_('title'), max_length=250, blank=True)
    items_count = models.PositiveSmallIntegerField(_('items count'), default=5)
    region_filter = models.CharField(
        _('filter by regions'),
        help_text=_('You can type more than one (separated with semicolon).'),
        max_length=250,
        blank=True
    )
    country_filter = models.CharField(
        _('filter by countries'),
        help_text=_('You can type more than one (separated with semicolon).'),
        max_length=250,
        blank=True
    )
    html_classes = models.CharField(_('HTML classes'), max_length=250, blank=True)

    def __str__(self):
        return self.title


def get_default_categories():
    return PolicyCategory.objects.active()


class RankingBrowserPluginModel(CMSPlugin):
    inst_col_name = models.CharField(_('Institution column name'), max_length=100)
    order_by = models.CharField(
        _('order by'), max_length=250, help_text=_('Specify field names separated by comma.'), blank=True
    )

    def __str__(self):
        return 'Ranking Browser'
