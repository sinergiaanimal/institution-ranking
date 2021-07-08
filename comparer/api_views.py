from rest_framework import viewsets

from comparer.models import *
from comparer.serializers import InstitutionListSerializer, InstitutionDetailSerializer, PolicyCategorySerializer


__all__ = ('PolicyCategoryViewSet', 'InstitutionViewSet')


class PolicyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PolicyCategory.objects.active()
    serializer_class = PolicyCategorySerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    queryset = Institution.objects.active().with_scores()

    def get_serializer_class(self):
        if self.action == 'list':
            return InstitutionListSerializer
        if self.action == 'retrieve':
            return InstitutionDetailSerializer
        return InstitutionListSerializer
