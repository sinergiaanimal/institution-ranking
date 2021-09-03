from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import BlogIndexPluginModel, BlogPost


@plugin_pool.register_plugin
class BlogIndexPluginPublisher(CMSPluginBase):
    model = BlogIndexPluginModel
    module = _('Blog')
    name = _('Blog Index')
    render_template = 'blog/cms/blog_index_plugin.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        
        posts = BlogPost.objects.active().order_by('-publication_date')
        context['feat_post'] = posts[0] if len(posts) else None
        context['posts'] = posts[1:]

        return context