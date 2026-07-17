from blog.models import Post
from django.db.models import Count, Q
from django.utils import timezone


def get_published_posts_queryset():
    return (
        Post.objects.select_related("author", "category", "location")
        .annotate(comment_count=Count("comments"))
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by("-pub_date")
    )


def get_posts_for_user(user):
    if user.is_authenticated:
        return (
            Post.objects.select_related("author", "category", "location")
            .annotate(comment_count=Count("comments"))
            .filter(
                Q(author=user)
                | (
                    Q(is_published=True)
                    & Q(category__is_published=True)
                    & Q(pub_date__lte=timezone.now())
                )
            )
            .order_by("-pub_date")
        )
    return get_published_posts_queryset()
