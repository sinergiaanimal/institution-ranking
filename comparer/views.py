from django.views.generic import DetailView

from .models import Institution


__all__ = ('InstitutionDetailView', )


class InstitutionDetailView(DetailView):
    model = Institution
    queryset = Institution.objects.active()
    context_object_name = 'institution'
    template_name = 'comparer/institution_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
