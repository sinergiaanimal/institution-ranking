from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import CoverPluginModel, EmbedPluginModel, WrapperPluginModel
from .forms import EmbedPluginForm


def concat_attrs(*attrs, separator=' '):
    """
    Helper function to join string attributes using separator.
    """
    return separator.join([attr for attr in attrs if attr])


@plugin_pool.register_plugin
class WrapperPluginPublisher(CMSPluginBase):
    model = WrapperPluginModel
    module = _('Common')
    name = _('Wrapper')
    render_template = 'common/cms/wrapper_plugin.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        instance.attributes['class'] = concat_attrs(
            'wrapper',
            instance.attributes.get('class'),
            separator=' '
        )
        return super().render(
            context, instance, placeholder
        )


@plugin_pool.register_plugin
class EmbedPluginPublisher(CMSPluginBase):
    model = EmbedPluginModel
    module = _('Common')
    name = _('Embed')
    render_template = 'common/cms/embed_plugin.html'
    change_form_template = 'djangocms_bootstrap4/admin/code.html'
    form = EmbedPluginForm
    allow_children = False


@plugin_pool.register_plugin
class CoverPluginPublisher(CMSPluginBase):
    model = CoverPluginModel
    module = _('Common')
    name = _('Cover')
    render_template = 'common/cms/cover_plugin.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        if instance.image:
            instance.attributes['style'] = concat_attrs(
                'background-image: url("{}")'.format(
                    instance.image.url
                ),
                instance.attributes.get('style'),
                separator='; '
            )
        instance.attributes['class'] = concat_attrs(
            'cover',
            instance.attributes.get('class'),
            separator=' '
        )

        context['darkness'] = '{:.2f}'.format(instance.darken / 100);

        return super().render(
            context, instance, placeholder
        )
