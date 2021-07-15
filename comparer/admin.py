import csv

from django import forms
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from common.csv_tools import CsvImporter, CsvColumn, CsvRelatedColumn, CsvImportError
from common.form_validators import validate_csv_ext
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


class InstitutionEmailInline(admin.TabularInline):
    model = InstitutionEmail
    extra = 0


class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 0


class InstitutionPolicyInline(admin.TabularInline):
    model = InstitutionPolicy
    extra = 0


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(validators=[validate_csv_ext])
    override_existing = forms.BooleanField(label=_('Override existing'), required=False)


class CsvInstitutionImporter(CsvImporter):
    model = Institution
    key_column_name = 'name'

    columns = [
        CsvColumn(name='name', field_name='name', required=True),
        CsvColumn(name='region', field_name='region', required=True),
        CsvColumn(name='country', field_name='country', required=True),
        CsvRelatedColumn(
            name='email', field_name='address', related_model=InstitutionEmail, fk_name='institution', many=True
        ),
        CsvRelatedColumn(
            name='facebook', field_name='url', related_model=SocialMediaLink, fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.FACEBOOK}
        ),
        CsvRelatedColumn(
            name='twitter', field_name='url', related_model=SocialMediaLink, fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.TWITTER}
        ),
        CsvRelatedColumn(
            name='instagram', field_name='url', related_model=SocialMediaLink, fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.INSTAGRAM}
        ),
        CsvRelatedColumn(
            name='linkedin', field_name='url', related_model=SocialMediaLink, fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.LINKEDIN}
        ),
        CsvRelatedColumn(
            name='youtube', field_name='url', related_model=SocialMediaLink, fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.YOUTUBE}
        ),
        CsvRelatedColumn(
            name='site', field_name='url', related_model=SocialMediaLink, fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.WEBSITE}
        )
    ]


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region', 'country', 'is_active', 'creation_timestamp', 'modification_timestamp']
    list_display_links = ['id', 'name']
    list_filter = ['is_active', 'region', 'creation_timestamp', 'modification_timestamp']
    search_fields = ['id', 'name', 'region', 'country']
    change_list_template = 'comparer/admin/institution_changelist.html'
    inlines = [
        InstitutionEmailInline,
        SocialMediaLinkInline,
        InstitutionPolicyInline,
    ]

    def get_urls(self):
        return [
            path(
                'import-institutions-csv/',
                self.import_institutions_csv,
                name='import-institutions-csv'
            ),
        ] + super().get_urls()

    def import_institutions_csv(self, request):
        if request.method == 'POST':
            form = CsvImportForm(request.POST, request.FILES)

            if form.is_valid():
                importer = CsvInstitutionImporter()
                try:
                    institutions = importer.import_data(
                        form.cleaned_data['csv_file'],
                        override_existing=form.cleaned_data['override_existing']
                    )
                except CsvImportError as e:
                    self.message_user(
                        request,
                        f'Institution import failed: {e}',
                        level=messages.ERROR
                    )
                else:
                    self.message_user(
                        request,
                        f'{len(institutions)} institutions has been successfully imported from csv file.'
                    )
                return redirect("..")

        else:  # GET
            form = CsvImportForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'view_name': _('Import institutions from csv')
        }
        return render(
            request, 'comparer/admin/csv_form.html', context
        )


admin.site.register(PolicyCategory, PolicyCategoryAdmin)
admin.site.register(PolicyCriterion, PolicyCriterionAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(SocialMediaLink)
admin.site.register(InstitutionEmail)
admin.site.register(InstitutionPolicy)
admin.site.register(MessageTemplate)
