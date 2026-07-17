from blog.models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect


class PostCheckMixin(UserPassesTestMixin):
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs[self.pk_url_kwarg])

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        post = self.get_object()
        return redirect("blog:post_detail", post_id=post.pk)


class PostMixin:
    model = Post
