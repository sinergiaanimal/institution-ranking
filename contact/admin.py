from django import forms
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from common.import_tools import CsvImporter, CsvFieldColumn, CsvRelatedColumn, CsvImportError, ZipImporter, CsvFKColumn
from common.form_validators import validate_csv_ext, validate_zip_ext
from .models import *


class ContactMessageAdmin(admin.ModelAdmin):
    model = ContactMessage
    list_display = [
        'id', 'sender_name', 'sender_email', 'status', 'creation_timestamp'
    ]
    list_display_links = ['id', 'sender_name']
    list_filter = ['status', 'creation_timestamp']
    search_fields = ['sender_name', 'sender_email']
    ordering = ['-creation_timestamp']
    readonly_fields = [
        'creation_timestamp', 'sender_name', 'sender_email', 'message',
        'status', 'status_msg', 'recipients'
    ]


admin.site.register(ContactMessage, ContactMessageAdmin)
