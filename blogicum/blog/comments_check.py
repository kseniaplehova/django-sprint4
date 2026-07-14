from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Post, Comment


def get_comment_and_check_permission(request, comment_id):
    """Получает комментарий и проверяет разрешение пользователя."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        raise Http404("Нет прав доступа к этому комментарию!")
    return comment


def render_comment_template(request, comment, form):
    """Рендерит шаблон комментария."""
    template = "blog/comment.html"
    context = {
        "comment": comment,
        "post": comment.post,
    }
    if form is not None:
        context["form"] = form
    return render(request, template, context)


def get_post(post_id):
    """Возвращает объект Post по ID."""
    return get_object_or_404(Post, id=post_id)
