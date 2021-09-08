from django.utils.translation import gettext as _
from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Recipient, ContactFormPluginModel


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0


@plugin_pool.register_plugin
class ContactFormPluginPublisher(CMSPluginBase):
    model = ContactFormPluginModel
    module = _('Contact')
    name = _('Contact Form')
    render_template = 'contact/cms/contact_form_plugin.html'
    inlines = [RecipientInline]

    def render(self, context, instance, placeholder):
        context.update({'plugin': instance})
        return context
