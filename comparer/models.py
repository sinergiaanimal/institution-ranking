from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from common.managers import ActivableModelQuerySet
from common.models import TimestampedModel, ActivableModel

__all__ = (
    'PolicyCategory', 'PolicyCriterion', 'Institution', 'SocialMediaLink', 'InstitutionEmail', 'InstitutionPolicy',
    'MessageTemplate', 'RankingBoxPluginModel',
)


class PolicyCategory(ActivableModel, TimestampedModel):
    name = models.CharField(_('name'), max_length=250)
    max_score = models.PositiveIntegerField(_('max_score'), default=0)
    # criterions - defined in comparer.models.InstitutionPolicy.criterion

    class Meta:
        verbose_name = _('Policy category')
        verbose_name_plural = _('Policy categories')

    def __str__(self):
        return self.name


class PolicyCriterion(ActivableModel, TimestampedModel):
    name = models.CharField(_('name'), max_length=250)
    category = models.ForeignKey(
        verbose_name=_('category'), to=PolicyCategory, on_delete=models.CASCADE,
        related_name='criterions'
    )
    # policies - defined in comparer.models.InstitutionPolicy.criterion

    class Meta:
        verbose_name = _('Policy criterion')
        verbose_name_plural = _('Policy criterions')

    def __str__(self):
        return self.name


class InstitutionQuerySet(ActivableModelQuerySet):

    def with_score(self):
        return self.annotate(score=models.Sum('policies__score'))


class Institution(ActivableModel, TimestampedModel):
    name = models.CharField(_('name'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    region = models.CharField(_('region'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100)
    logo = models.ImageField(_('logo'), upload_to='comparer/institution/logo', blank=True)
    # social_media_links = defined in comparer.models.SocialMediaLink.institution
    # emails = defined in comparer.models.InstitutionEmail.institution
    # policies = defined in comparer.models.InstitutionPolicy.institution
    objects = InstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')

    def __str__(self):
        return self.name


class SocialMediaLink(ActivableModel, TimestampedModel):
    FACEBOOK, INSTAGRAM, TWITTER, EMAIL, ANOTHER = range(1, 6)
    KIND_CHOICES = (
        (FACEBOOK, _('Facebook')),
        (INSTAGRAM, _('Instagram')),
        (TWITTER, _('Twitter')),
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


class InstitutionPolicy(ActivableModel, TimestampedModel):
    institution = models.ForeignKey(
        verbose_name=_('institution'), to=Institution, on_delete=models.CASCADE,
        related_name='policies'
    )
    criterion = models.ForeignKey(
        verbose_name=_('policy criterion'), to=PolicyCriterion, on_delete=models.CASCADE,
        related_name='policies'
    )
    title = models.CharField(_('title'), max_length=250)
    link = models.URLField(_('link'), blank=True)
    text = models.TextField(_('text'), blank=True)
    comment = models.TextField(_('comment'), blank=True)
    score = models.IntegerField(_('score'), default=0)

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


# class RankingBrowserPluginModel(CMSPlugin):
#
#     def __str__(self):
#         return 'comparer'
