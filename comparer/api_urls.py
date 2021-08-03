from django.urls import path

from .api_views import *


urlpatterns = (
    path(
        'message-templates/',
        MessageTemplateList.as_view(),
        name='message-templates'
    ),
    path(
        # TODO: Do we need this?
        'message-templates/for-score/<int:score>/',
        MessageTemplateListForScore.as_view(),
        name='message-templates-for-score'
    ),
)
