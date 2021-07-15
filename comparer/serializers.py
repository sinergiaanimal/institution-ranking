from django.conf import settings

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField

from comparer.models import *


class PolicyCriterionNestedSerializer(ModelSerializer):

    class Meta:
        model = PolicyCriterion
        fields = [
            'id', 'name', 'order'
        ]


class PolicyCategorySerializer(ModelSerializer):
    criterions = SerializerMethodField()

    class Meta:
        model = PolicyCategory
        fields = [
            'id', 'slug', 'name', 'order', 'max_score', 'criterions'
        ]

    def get_criterions(self, obj):
        return PolicyCriterionNestedSerializer(
            obj.criterions.active(), many=True
        ).data


class InstitutionListSerializer(ModelSerializer):
    scores = SerializerMethodField()
    logo_thumb = ImageField()

    class Meta:
        model = Institution
        fields = [
            'id', 'name', 'region', 'country', 'logo', 'logo_thumb', 'scores'
        ]

    def get_scores(self, obj):
        scores = {
            'total': obj.score_total
        }
        for slug in settings.POLICY_CATEGORY_SLUGS:
            scores[slug] = getattr(obj, f'score_{slug}')
        return scores


class InstitutionDetailSerializer(ModelSerializer):
    emails = SerializerMethodField()

    class Meta:
        model = Institution
        fields = [
            'name', 'region', 'country', 'logo', 'logo_thumb',
            'social_media_links', 'emails', 'policies',

            'description',
        ]
