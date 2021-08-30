from django.contrib import admin

from cms.admin.placeholderadmin import PlaceholderAdminMixin

from common.models import ContentPlaceholder


class ContentPlaceholderAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ['slug', 'creation_timestamp', 'modification_timestamp']
    search_fields = ['slug', 'description']
    list_filter = ['creation_timestamp', 'modification_timestamp']


admin.site.register(ContentPlaceholder, ContentPlaceholderAdmin)
