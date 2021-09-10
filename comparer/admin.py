from django import forms
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from common.import_tools import CsvImporter, CsvFieldColumn, CsvRelatedColumn, CsvImportError, ZipImporter, CsvFKColumn
from common.form_validators import validate_csv_ext, validate_zip_ext
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
    list_display = [
        'id', 'slug', 'name', 'short_name', 'order', 'max_score', 'is_active'
        ]
    list_display_links = ['id', 'slug']
    lift_filter = ['is_active']
    search_fields = ['name', 'short_name']
    ordering = ['order', 'name']
    prepopulated_fields = {'slug': ('short_name',)}
    inlines = [
        PolicyCriterionInline,
    ]


class InstitutionEmailInline(admin.TabularInline):
    model = InstitutionEmail
    extra = 0


class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 0


class InstitutionScoreInline(admin.TabularInline):
    model = InstitutionScore
    extra = 0


class CsvImportForm(forms.Form):
    D_COLON = ','
    D_SEMICOLON = ';'
    DELIMITER_CHOICES = (
        (D_COLON, _('colon: ","')),
        (D_SEMICOLON, _('semicolon: ";"'))
    )

    csv_file = forms.FileField(validators=[validate_csv_ext])
    delimiter = forms.ChoiceField(
        label=_('CSV column delimiter'), required=True,
        choices=DELIMITER_CHOICES, initial=D_SEMICOLON
    )
    override_existing = forms.BooleanField(
        label=_('Override existing'), required=False
    )

class ArchiveImportForm(forms.Form):
    archive_file = forms.FileField(validators=[validate_zip_ext])


def remove_institution_related_data(instance, global_data):
    instance.social_media_links.all().delete()
    instance.emails.all().delete()


class CsvInstitutionImporter(CsvImporter):
    model = Institution
    key_column_name = 'name'

    columns = [
        CsvFieldColumn(name='name', field_name='name', required=True),
        CsvFieldColumn(name='region', field_name='region', required=True),
        CsvFieldColumn(name='country', field_name='country', required=True),
        CsvRelatedColumn(
            name='email', field_name='address', related_model=InstitutionEmail,
            fk_name='institution', many=True
        ),
        CsvRelatedColumn(
            name='facebook', field_name='url', related_model=SocialMediaLink,
            data_type=CsvFieldColumn.DT_LINK,
            fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.FACEBOOK}
        ),
        CsvRelatedColumn(
            name='twitter', field_name='url', related_model=SocialMediaLink,
            data_type=CsvFieldColumn.DT_LINK,
            fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.TWITTER}
        ),
        CsvRelatedColumn(
            name='instagram', field_name='url', related_model=SocialMediaLink,
            data_type=CsvFieldColumn.DT_LINK,
            fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.INSTAGRAM}
        ),
        CsvRelatedColumn(
            name='linkedin', field_name='url', related_model=SocialMediaLink,
            data_type=CsvFieldColumn.DT_LINK,
            fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.LINKEDIN}
        ),
        CsvRelatedColumn(
            name='youtube', field_name='url', related_model=SocialMediaLink,
            data_type=CsvFieldColumn.DT_LINK,
            fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.YOUTUBE}
        ),
        CsvRelatedColumn(
            name='site', field_name='url', related_model=SocialMediaLink,
            data_type=CsvFieldColumn.DT_LINK,
            fk_name='institution', many=False,
            related_data={'kind': SocialMediaLink.WEBSITE}
        )
    ]

    processors = {
        4: [remove_institution_related_data]
    }


def process_institution_score(instance, global_data):
    institution = global_data['institution name']
    criterion = global_data['criterion']
    try:
        score = InstitutionScore.objects.get(institution=institution, criterion=criterion)
    except InstitutionScore.DoesNotExist:
        score = InstitutionScore(
            institution=institution,
            criterion=criterion
        )

    score_val = global_data.get('score')
    if score_val is not None:
        score.score = score_val

    comment = global_data.get('comment')
    if comment is not None:
        score.comment = comment

    score.save()

    instance.score = score


class CsvPolicyImporter(CsvImporter):
    model = InstitutionPolicy
    key_column_name = 'dummy'

    columns = [
        CsvFKColumn(
            name='institution name', field_name=None, related_model=Institution, key_field_name='name',
            required=True, save_globally=True, do_assign=False, priority=4
        ),
        CsvFKColumn(
            name='criterion', field_name=None, related_model=PolicyCriterion, key_field_name='name',
            required=True, save_globally=True, do_assign=False, priority=4
        ),
        CsvFieldColumn(
            name='policy', field_name='title'
        ),
        CsvFieldColumn(
            name='link of policy', field_name='link',
            data_type=CsvFieldColumn.DT_LINK
        ),
        CsvFieldColumn(
            name='text of policy', field_name='text', data_type=CsvFieldColumn.DT_MARKDOWN
        ),
        CsvFieldColumn(
            name='comment', field_name='score__comment', do_assign=False, save_globally=True, priority=4
        ),
        CsvFieldColumn(
            name='score', field_name='score__score', data_type=CsvFieldColumn.DT_NUMBER,
            do_assign=False, save_globally=True, priority=4
        )
    ]

    processors = {
        4: [process_institution_score]
    }

    def pre_import(self, override_existing=False):
        if override_existing:
            InstitutionPolicy.objects.all().delete()


class InstitutionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'slug', 'name', 'region', 'country', 'is_active',
        'creation_timestamp', 'modification_timestamp'
    ]
    list_display_links = ['id', 'slug', 'name']
    list_filter = ['is_active', 'region', 'creation_timestamp', 'modification_timestamp']
    search_fields = ['id', 'name', 'region', 'country']
    change_list_template = 'comparer/admin/institution_changelist.html'
    inlines = [
        InstitutionEmailInline,
        SocialMediaLinkInline,
        InstitutionScoreInline,
    ]

    def get_urls(self):
        return [
            path(
                'import-institutions-csv/',
                self.import_institutions_csv,
                name='import-institutions-csv'
            ),
            path(
                'import-policies-csv/',
                self.import_policies_csv,
                name='import-policies-csv'
            ),
            path(
                'import-logo-zip/',
                self.import_logo_zip,
                name='import-logo-zip'
            ),
        ] + super().get_urls()

    def import_logo_zip(self, request):
        if request.method == 'POST':
            form = ArchiveImportForm(request.POST, request.FILES)

            if form.is_valid():
                importer = ZipImporter(
                    model=Institution, file_fname='logo', query_fname='name',
                    allowed_ext=['bmp', 'gif', 'png', 'jpg', 'jpeg', 'ico']
                )
                imported_count, errors_list, unrecog_list = importer.import_data(form.cleaned_data['archive_file'])

                message = _('Successfully assigned logo files to {} institutions.').format(imported_count)
                if errors_list:
                    message += _(' Encountered errors while processing: "{}".').format('", "'.join(errors_list))
                if unrecog_list:
                    message += _(' Unrecognized files in the archive: "{}".').format('", "'.join(unrecog_list))
                self.message_user(request, message)

                return redirect("..")

        else:  # GET
            form = ArchiveImportForm()

        title = _('Import logo from zip')
        context = {
            'form': form,
            'opts': self.model._meta,
            'title': title,
            'view_name': title,
            'submit_btn_name': _('Upload ZIP')
        }
        return render(
            request, 'comparer/admin/file_upload_form.html', context
        )

    def import_institutions_csv(self, request):
        if request.method == 'POST':
            form = CsvImportForm(request.POST, request.FILES)

            if form.is_valid():
                importer = CsvInstitutionImporter()
                try:
                    institutions = importer.import_data(
                        form.cleaned_data['csv_file'],
                        delimiter=form.cleaned_data['delimiter'],
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

        title = _('Import institutions from csv')
        context = {
            'form': form,
            'opts': self.model._meta,
            'title': title,
            'view_name': title,
            'submit_btn_name': _('Upload CSV')
        }
        return render(
            request, 'comparer/admin/file_upload_form.html', context
        )

    def import_policies_csv(self, request):
        if request.method == 'POST':
            form = CsvImportForm(request.POST, request.FILES)

            if form.is_valid():
                importer = CsvPolicyImporter()
                try:
                    policies = importer.import_data(
                        form.cleaned_data['csv_file'],
                        delimiter=form.cleaned_data['delimiter'],
                        override_existing=form.cleaned_data['override_existing']
                    )
                except CsvImportError as e:
                    self.message_user(
                        request,
                        f'Policies import failed: {e}',
                        level=messages.ERROR
                    )
                else:
                    self.message_user(
                        request,
                        f'{len(policies)} policies has been successfully imported from csv file.'
                    )
                return redirect("..")

        else:  # GET
            form = CsvImportForm()

        title = _('Import institutions from csv')
        context = {
            'form': form,
            'opts': self.model._meta,
            'title': title,
            'view_name': title,
            'submit_btn_name': _('Upload CSV')
        }
        return render(
            request, 'comparer/admin/file_upload_form.html', context
        )


class InstitutionPolicyInline(admin.TabularInline):
    model = InstitutionPolicy
    extra = 0


class InstitutionScoreAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'institution', 'criterion', 'score', 'is_active', 'creation_timestamp', 'modification_timestamp'
    ]
    list_filter = ['criterion', 'is_active', 'score', 'is_active', 'creation_timestamp', 'modification_timestamp']
    search_fields = ['institution__name', 'criterion__name', 'score']
    inlines = [InstitutionPolicyInline]


class InstitutionPolicyAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'score', 'title', 'link', 'is_active', 'creation_timestamp', 'modification_timestamp'
    ]
    list_filter = [
        'score__score', 'is_active', 'creation_timestamp', 'modification_timestamp'
    ]
    search_fields = ['title']


class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'institution', 'kind', 'url'
    ]
    list_filter = ['kind']
    search_fields = ['institution__name', 'url']


admin.site.register(PolicyCategory, PolicyCategoryAdmin)
admin.site.register(PolicyCriterion, PolicyCriterionAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)
admin.site.register(InstitutionEmail)
admin.site.register(InstitutionScore, InstitutionScoreAdmin)
admin.site.register(InstitutionPolicy, InstitutionPolicyAdmin)
admin.site.register(MessageTemplate)
