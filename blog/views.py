from django.views.generic import DetailView

from .models import BlogPost

__all__ = ('BlogPostDetailView',)


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