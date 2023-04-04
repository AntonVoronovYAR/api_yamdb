from datetime import date

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

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class AuthSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
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
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
