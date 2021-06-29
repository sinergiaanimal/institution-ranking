import operator
from functools import reduce

from django.utils.translation import gettext as _
from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import RankingBoxPluginModel, Institution


@plugin_pool.register_plugin
class PollPluginPublisher(CMSPluginBase):
    model = RankingBoxPluginModel
    module = _('Comparer')
    name = _('Ranking Box')
    render_template = 'comparer/cms/ranking_box_plugin.html'

    def render(self, context, instance, placeholder):
        institutions = Institution.objects.with_score()

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

        institutions = institutions.order_by('-score')[:instance.items_count]

        context.update({'instance': instance, 'institutions': institutions})

        return context
