from django.contrib import admin

from .models import *


class PolicyCriterionAdmin(admin.ModelAdmin):
    model = PolicyCriterion
    list_display = ['id', 'name', 'order', 'category', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category__name']
    ordering = ['category', 'order', 'name']


class PolicyCriterionInline(admin.TabularInline):
    model = PolicyCriterion
    extra = 0


class PolicyCategoryAdmin(admin.ModelAdmin):
    model = PolicyCategory
    list_display = ['id', 'slug', 'name', 'order', 'max_score', 'is_active']
    list_display_links = ['id', 'slug', 'name']
    lift_filter = ['is_active']
    search_fields = ['name']
    ordering = ['order', 'name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        PolicyCriterionInline,
    ]


class InstitutionPolicyInline(admin.TabularInline):
    model = InstitutionPolicy
    extra = 0


class InstitutionAdmin(admin.ModelAdmin):
    inlines = [
        InstitutionPolicyInline,
    ]


admin.site.register(PolicyCategory, PolicyCategoryAdmin)
admin.site.register(PolicyCriterion, PolicyCriterionAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(SocialMediaLink)
admin.site.register(InstitutionEmail)
admin.site.register(InstitutionPolicy)
admin.site.register(MessageTemplate)
