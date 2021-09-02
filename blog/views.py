from django.views.generic import DetailView

from .models import BlogPost

__all__ = ('BlogPostDetailView',)


class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.active()
    context_object_name = 'post'
    template_name = 'blog/blog_post_detail.html'

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        if not self.request.user.is_staff:
            # Only staff users should be able to see inactive posts.
            queryset = queryset.active()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bg_opacity'] =  '{:.2f}'.format(
            context['post'].header_darken / 100
        )
        return context