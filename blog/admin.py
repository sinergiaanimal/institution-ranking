from django.contrib import admin

from cms.admin.placeholderadmin import PlaceholderAdminMixin

from .models import BlogPost


class BlogPostAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = (
        'id', 'slug', 'title', 'publication_date', 'reading_time',
        'creation_timestamp', 'modification_timestamp', 'is_active'
    )
    list_display_links = ('id', 'slug')
    list_filter = (
        'publication_date',
        'creation_timestamp', 'modification_timestamp', 'is_active'
    )
    search_fields = ('id', 'slug', 'title')


admin.site.register(BlogPost, BlogPostAdmin)
