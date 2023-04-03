from rest_framework.viewsets import ModelViewSet
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from reviews.models import Category, Genre, Title, Review
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, UserSerializer)
from users.models import User

from .serializers import (CommentSerializer, ReviewSerializer,
                          UserSerializer)
from .permissions import (AdminOrReadOnly, AdminOrSuperuser,
                          AuthorOrAuthenticated, AdminModerAuthorOrReadOnly)
from .mixins import ListCreateDestroyViewSet
from .filters import TitleFilter


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [AdminOrReadOnly]

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering = ['username']
    search_fields = ['username']

    @action(detail=False,
            methods=('get', 'patch'),
            url_path=r'me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrAuthenticated,
                          AdminModerAuthorOrReadOnly,
                          AdminOrReadOnly, AdminOrSuperuser]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrAuthenticated,
                          AdminModerAuthorOrReadOnly,
                          AdminOrReadOnly, AdminOrSuperuser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
