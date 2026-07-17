from http import HTTPStatus

from django.shortcuts import render
from django.views.generic import TemplateView


def page_not_found(request, exception):
    """Обработчик для страницы 404 Not Found."""
    return render(request, "pages/404.html", status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=""):
    """Обработчик для ошибки CSRF."""
    return render(request, "pages/403csrf.html", status=HTTPStatus.FORBIDDEN)


def error500(request, *args, **kwargs):
    """Обработчик для серверной ошибки 500."""
    return render(
        request, "pages/500.html", status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


class About(TemplateView):
    """Отображает страницу "О проекте"."""

    template_name = "pages/about.html"


class Rules(TemplateView):
    """Отображает страницу "Наши правила"."""

    template_name = "pages/rules.html"
