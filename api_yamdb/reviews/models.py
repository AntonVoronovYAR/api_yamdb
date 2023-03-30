from django.db import models

MAX_TEXT_LEN: int = 25


class Category(models.Model):
    name = models.CharField(max_length=256, help_text='Наименование')
    slug = models.SlugField(max_length=50, help_text='Тип')

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class Genre(models.Model):
    name = models.CharField(max_length=256, help_text='Наименование')
    slug = models.SlugField(max_length=50, help_text='Тип')

    def __str__(self):
        return self.name[:MAX_TEXT_LEN]


class Title(models.Model):
    name = models.CharField(max_length=256, help_text='Название')
    year = models.IntegerField(help_text='Год выпуска')
    description = models.TextField(help_text='Описание', blank=True)
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
