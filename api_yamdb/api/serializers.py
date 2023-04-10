from datetime import date

from django.contrib.auth.models import AbstractUser
from rest_framework import filters, serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    class Meta:
        exclude = ['id']
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    class Meta:
        exclude = ['id']
        lookup_field = 'slug'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError('Проверьте год издания!')
        return value


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class AuthSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[AbstractUser.username_validator, ]
    )
    email = serializers.EmailField(max_length=254, required=True)

    # Комментарий для ревьювера. Артем, не до конца понял как тут надо
    # выносить в переменную. Ведь у меня используется 2 разных метода:
    # в одном случае использую
    # filter (с username и email), в другом get(c username и email)
    # в итоге пришлось поменять get на filter, получилось вот так
    # Также ознакомился с Q объектами, смысл понятен: в одном filter используем
    # при необходимости несколько условий AND, OR, NOT.
    # Но методы exists() и first()
    # в данном случае не поддерживаются, направь, пожалуйста,
    # что не так делаю?:
    # user(Q(username=username).exists() |
    # Q(username=username).first().email != email):
    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_username = User.objects.filter(username=username)
        user_email = User.objects.filter(email=email)
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"!')
        if user_username.exists() and user_username.first().email != email:
            raise serializers.ValidationError(f'Поле {email} не совпадает!')
        if user_email.exists() and user_email.first().username != username:
            raise serializers.ValidationError(f'Поле {username} не совпадает!')
        return data


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        if request.stream.method == 'POST':
            if Review.objects.filter(
                    title=title_id,
                    author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
