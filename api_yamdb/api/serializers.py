from django.db.models import Avg
from rest_framework import filters, serializers
from reviews.models import Category, Genre, Title


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
    #     rating = Review.objects.filter(pk=obj.id).aggregate(Avg('score'))
    #     return rating['score']
