from django.db import models

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


MAX_TEXT_LEN: int = 25
User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование'
    )
    slug = models.SlugField(max_length=50, help_text='Тип')

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование'
    )
    slug = models.SlugField(max_length=50, help_text='Тип')

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class Title(models.Model):
    name = models.CharField(max_length=256, help_text='Название')
    year = models.IntegerField(help_text='Год выпуска')
    # пока закомментировал, так как нужна модель Review
    # rating = models.ForeignKey(
    #     Review,
    #     on_delete=models.CASCADE,
    #     help_text='Рейтинг',
    #     default=None
    # )
    description = models.TextField(help_text='Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class ParentingModel(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Review(ParentingModel):
    """Отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Отзывы'
        unique_together = ('author', 'title',)


class Comment(ParentingModel):
    """Комментарии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарии'
        ordering = ['id', ]
