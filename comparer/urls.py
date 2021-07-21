from django.urls import path

from .views import *


urlpatterns = (
    path('institutions/<slug:slug>/', InstitutionDetailView.as_view(), name='institution-detail'),
)
