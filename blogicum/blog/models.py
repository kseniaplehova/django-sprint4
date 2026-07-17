from core.constants import SLUG_LENGTH, TEXT_LENGTH, TITLE_LENGTH
from core.models import AuthorModel, CreatedAtModel, PublishedModel, TitleModel
from django.db import models


class Category(PublishedModel, TitleModel):
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        max_length=SLUG_LENGTH,
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )

    class Meta(PublishedModel.Meta):
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ("title",)


class Location(PublishedModel):
    name = models.CharField("Название места", max_length=TITLE_LENGTH)

    class Meta(PublishedModel.Meta):
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Post(PublishedModel, TitleModel, AuthorModel):
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    image = models.ImageField(
        "Изображение", upload_to="post_images", blank=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )

    class Meta(PublishedModel.Meta):
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)
        default_related_name = "%(class)ss"


class Comment(CreatedAtModel, AuthorModel):
    text = models.TextField("Текст комментария")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="Пост"
    )

    class Meta(CreatedAtModel.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        default_related_name = "%(class)ss"

    def __str__(self):
        return self.text[:TEXT_LENGTH]
