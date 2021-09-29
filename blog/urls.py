from django.urls import path

from .views import *


urlpatterns = (
    path('<slug:slug>/<str:action>/',
        BlogPostActionView.as_view(),
        name='blog-post-action'
    ),
    path('<slug:slug>/',
        BlogPostDetailView.as_view(),
        name='blog-post-detail'
    ),
)
