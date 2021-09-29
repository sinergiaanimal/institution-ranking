from django.views.generic import DetailView
from django.views import View
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

from .models import BlogPost

__all__ = ('BlogPostDetailView', 'BlogPostActionView')


class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.active()
    context_object_name = 'post'
    template_name = 'blog/blog_post_detail.html'
    recent_post_count = 3

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        if not self.request.user.is_staff:
            # Only staff users should be able to see inactive posts.
            queryset = queryset.active()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        recent_posts = BlogPost.objects.all().exclude(
            pk=context['post'].pk
        ).order_by('-publication_date')

        if not self.request.user.is_staff:
            recent_posts = recent_posts.active()
        
        context['recent_posts'] = recent_posts[:self.recent_post_count]

        context['post_uri'] = self.request.build_absolute_uri(
            self.request.get_full_path()
        )
        return context


@method_decorator(permission_required('blog.change_blogpost'), name='dispatch')
class BlogPostActionView(View):

    def post(self, request, slug, action, *args, **kwargs):
        if action not in ('publish', 'unpublish'):
            return HttpResponseBadRequest(f'Action "{action}" is not allowed.')
        blogpost = get_object_or_404(BlogPost, slug=slug)

        if action == 'publish':
            blogpost.is_active = True
        elif action == 'unpublish':
            blogpost.is_active = False
        blogpost.save()

        return redirect(blogpost)
