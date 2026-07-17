from core.constants import TITLE_LENGTH
from django.contrib.auth.models import User
from django.db import models


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class PublishedModel(CreatedAtModel):
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )

    class Meta(CreatedAtModel.Meta):
        abstract = True


class TitleModel(models.Model):
    title = models.CharField("Заголовок", max_length=TITLE_LENGTH)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title[:TITLE_LENGTH]


class AuthorModel(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.author.username
