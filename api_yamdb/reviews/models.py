from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .const import MAX_TEXT_LEN

User = get_user_model()


class Category(models.Model):
    """Категории."""

    name = models.CharField(max_length=256, help_text='Наименование')
    slug = models.SlugField(max_length=50, help_text='Тип', unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(max_length=256, help_text='Наименование')
    slug = models.SlugField(max_length=50, help_text='Тип', unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=256,
        help_text='Название',
        db_index=True
    )
    year = models.IntegerField(help_text='Год выпуска', db_index=True)
    description = models.TextField(help_text='Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class GenreTitle(models.Model):
    """Жанры/Произведения."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Отзывы."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]
        ordering = ['pub_date']

    def __str__(self):
        return f'{self.text}, {self.score}'


class Comment(models.Model):
    """Комментарии."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text}'
