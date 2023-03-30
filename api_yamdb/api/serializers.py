from django.db.models import Avg
from rest_framework import filters, serializers
from reviews.models import Category, Genre, Title, Comment, Review
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    # def get_rating(self, obj):
    #    rating = Re
    #     rating = Review.objects.filter(pk=obj.id).aggregate(Avg('score'))
    #     return rating['score']





class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        read_only_fields = ('id', 'title', 'pub_date')
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        is_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Пользователь уже оставлял отзыв на это произведение')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментариев
    """
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        read_only_fields = ('id', 'review', 'pub_date')
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
