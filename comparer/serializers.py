from django.conf import settings

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField

from comparer.models import *


__all__ = (
    'PolicyCategorySerializer', 'InstitutionListSerializer', 'InstitutionDetailSerializer',
    'MessageTemplateSerializer'
)


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
            'id', 'slug', 'name', 'short_name',
            'order', 'max_score', 'criterions'
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
            'id', 'slug', 'name', 'region', 'country', 'logo', 'logo_thumb', 'scores'
        ]

    def get_scores(self, obj):
        scores = {
            'total': obj.score_total
        }
        for slug in settings.POLICY_CATEGORY_SLUGS:
            scores[slug] = getattr(obj, f'score_{slug}')
        return scores


class SocialMediaLinkSerializer(ModelSerializer):
    kind_name = SerializerMethodField()

    class Meta:
        model = SocialMediaLink
        fields = ['id', 'kind', 'kind_name', 'url']

    def get_kind_name(self, obj):
        return obj.get_kind_display()


class InstitutionEmailSerializer(ModelSerializer):

    class Meta:
        model = InstitutionEmail
        fields = ['id', 'address']


class InstitutionDetailSerializer(InstitutionListSerializer):
    social_media_links = SocialMediaLinkSerializer(many=True)
    emails = InstitutionEmailSerializer(many=True)

    class Meta:
        model = Institution
        fields = InstitutionListSerializer.Meta.fields + [
            'social_media_links', 'emails', 'description',
        ]


class MessageTemplateSerializer(ModelSerializer):

    class Meta:
        model = MessageTemplate
        fields = [
            'id', 'kind', 'min_score', 'max_score',
            'title', 'content'
        ]
