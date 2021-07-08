from cms.sitemaps import CMSSitemap

from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path, include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.contrib.sitemaps.views import sitemap

from rest_framework import routers

from comparer.api_views import *


urlpatterns = i18n_patterns(
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    re_path(r'^admin/', admin.site.urls),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}
    ),
)


router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'policy-categories', PolicyCategoryViewSet)

urlpatterns += (
    re_path(r'^api/', include(router.urls)),
)


if settings.SERVE_MEDIA:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    re_path(r'^', include('cms.urls')),
)


