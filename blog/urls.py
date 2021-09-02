from django.urls import path

from .views import *


urlpatterns = (
    path('<slug:slug>/',
        BlogPostDetailView.as_view(),
        name='blog-post-detail'
    ),
)
