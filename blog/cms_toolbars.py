import re

from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _

from cms.utils.urlutils import admin_reverse
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import LinkItem

from .models import BlogPost


class PostItem(LinkItem):
    template = 'blog/cms/toolbar_post_item.html'

    def get_context(self):
        context = super().get_context()
        context['csrf_token'] = self.toolbar.csrf_token
        return context


@toolbar_pool.register
class BlogToolbar(CMSToolbar):

    def post_template_populate(self):
        self.toolbar.add_sideframe_item(
            name=_('Blog'),
            url=admin_reverse('blog_blogpost_changelist')
        )

        if self.is_current_app:
            matched = re.match(r'^/blog/(?P<slug>[-\w]+)/$', self.request.path)
            if matched:
                slug = matched.groupdict()['slug']
                blogpost = BlogPost.objects.get(
                    slug=slug
                )
                is_active = blogpost.is_active
                self.toolbar.add_item(
                    item=PostItem(
                    name=_('Unpublish') if is_active else _('Publish'),
                    side=self.toolbar.RIGHT,
                        url=reverse(
                            'blog-post-action',
                            kwargs={
                                'slug': slug,
                                'action': 'unpublish' if is_active else 'publish'
                            },
                        )
                    )
                )
