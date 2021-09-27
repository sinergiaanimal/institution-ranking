from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import BlogIndexPluginModel, BlogRecentPluginModel, BlogPost


@plugin_pool.register_plugin
class BlogIndexPluginPublisher(CMSPluginBase):
    model = BlogIndexPluginModel
    module = _('Blog')
    name = _('Blog Index')
    render_template = 'blog/cms/blog_index_plugin.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        
        posts = BlogPost.objects.all().order_by('-publication_date')
        if not context['request'].user.is_staff:
            posts = posts.active()

        context['feat_post'] = posts[0] if len(posts) else None
        context['posts'] = posts[1:]

        return context


@plugin_pool.register_plugin
class BlogRecentPluginPublisher(CMSPluginBase):
    model = BlogRecentPluginModel
    module = _('Blog')
    name = _('Recent Blog Posts')
    render_template = 'blog/cms/blog_recent_plugin.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        
        context['posts'] = BlogPost.objects.active().order_by(
            '-publication_date'
        )[:instance.post_count]
        
        return context