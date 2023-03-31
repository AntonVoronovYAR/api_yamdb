from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, GenreTitle, Title, Comment, Review
from users.models import User

FILE_DATA_TO_MODEL: dict = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):

    def write_data_to_model(self, file, model):
        with open(f'static/data/{file}', encoding='utf-8') as f:
            rows = DictReader(f)
            for row in rows:
                if model == Title:
                    category_obj = Category.objects.get(pk=row['category'])
                    del row['category']
                    model.objects.get_or_create(**row, category=category_obj)
                elif model == Review or model == Comment:
                    author_obj = User.objects.get(pk=row['author'])
                    del row['author']
                    model.objects.get_or_create(**row, author=author_obj)
                else:
                    model.objects.get_or_create(**row)

    def handle(self, *args, **options):
        for file, model in FILE_DATA_TO_MODEL.items():
            self.write_data_to_model(file, model)
