from django.views.generic import DetailView
from django.db import models

from common.models import ContentPlaceholder
from .models import Institution, PolicyCategory


__all__ = ('InstitutionDetailView', )


class InstitutionDetailView(DetailView):
    model = Institution
    queryset = Institution.objects.active().with_scores()
    context_object_name = 'institution'
    template_name = 'comparer/institution_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = [
            {'instance': obj} for obj in PolicyCategory.objects.active()
        ]
        context['score_max'] = PolicyCategory.objects.active().aggregate(
            models.Sum('max_score')
        )['max_score__sum']
        context['score_current'] = self.object.score_total
        context['score_percentage'] = round(
            (context['score_current'] or 0) * 100 / context['score_max']
        )

        # gathering additional data
        for cat_dict in categories:
            cat = cat_dict['instance']
            cat_dict['score_max'] = cat.max_score
            cat_dict['score_current'] = getattr(
                self.object, f'score_{cat.slug}'
            )

            cat_dict['score_percentage'] = round(
                (cat_dict['score_current'] or 0) * 100 / cat_dict['score_max']
            ) if cat_dict['score_max'] else 0
            cat_dict['scores'] = self.object.scores.active().filter(
                criterion__category=cat
            )

        context['categories'] = categories

        context['placeholders'] = {}
        for slug in [
            'inst_detail_card_header_bg',
            'inst_detail_policy_name_header',
            'inst_detail_policy_text_header'
        ]:
            context['placeholders'][slug] = \
                ContentPlaceholder.objects.get_or_create(slug=slug)[0]

        return context
