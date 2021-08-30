import operator
from functools import reduce

from django.utils.translation import gettext as _
from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from .models import (
    PolicyCategory, RankingBoxPluginModel, Institution, RankingBrowserPluginModel
)


@plugin_pool.register_plugin
class RankingBoxPluginPublisher(CMSPluginBase):
    model = RankingBoxPluginModel
    module = _('Comparer')
    name = _('Ranking Box')
    render_template = 'comparer/cms/ranking_box_plugin.html'

    def render(self, context, instance, placeholder):
        institutions = Institution.objects.with_scores()

        if instance.region_filter:
            institutions = institutions.filter(
                reduce(
                    operator.or_,
                    [Q(region__iexact=c) for c in instance.region_filter.split(';')]
                )
            )

        if instance.country_filter:
            institutions = institutions.filter(
                reduce(
                    operator.or_,
                    [Q(country__iexact=c) for c in instance.country_filter.split(';')]
                )
            )

        institutions = institutions.order_by('-score_total')[:instance.items_count]

        context.update({'instance': instance, 'institutions': institutions})

        return context


@plugin_pool.register_plugin
class RankingBrowserPluginPublisher(CMSPluginBase):
    model = RankingBrowserPluginModel
    module = _('Comparer')
    name = _('Ranking Browser')
    render_template = 'comparer/cms/ranking_browser_plugin.html'

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context


@plugin_pool.register_plugin
class CriteriaPluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Comparer')
    name = _('Criteria Scoring')
    render_template = 'comparer/cms/criteria_plugin.html'

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'categories': PolicyCategory.objects.active().prefetch_related('criterions')
        })
        return context


