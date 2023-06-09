from django.core.mail import EmailMessage
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, Comment
from users.models import User
from api.serializers import (AuthSignUpSerializer, AuthTokenSerializer,
                             CategorySerializer, GenreSerializer,
                             TitleSerializer)
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (AdminModerAuthorOrReadOnly, AdminOrReadOnly,
                          AdminOrSuperuser)
from .serializers import (CommentSerializer, NotAdminSerializer,
                          ReviewSerializer, UserSerializer)
from users.functions import create_confirmation_code


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Разрешенные методы GET, PUT, DELETE.

    Права на изменения только у Админа.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Разрешенные методы GET, PUT, DELETE.

    Права на изменения только у Админа.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """
    Разрешены все методы.

    Но права на изменения только у Админа.
    """

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
    """
    Разрешены методы GET, PATCH, POST, DELETE.

    Права только у администратора. Получение/изменение
    данных своей учетной записи - авторизованный пользователь
    """

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOrSuperuser,)
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering = ['username']
    search_fields = ['username']
    http_method_names = ['get', 'patch', 'post', 'delete']

    @action(detail=False,
            methods=('get', 'patch'),
            url_path='me',
            permission_classes=(IsAuthenticated,))
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.

    Права доступа: Доступно без токена.
    """

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email.

    Права доступа: Доступно без токена.
    """

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = AuthSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = create_confirmation_code()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтверждения для доступа к API: {confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API!'
        }
        APISignup.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Разрешенные методы GET, POST, PATCH, DELETE.

    Права доступа: GET - Доступно без токена.
    POST - Аутентифицированные пользователи
    PATCH, DELETE - Автор, модер, админ
    """

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        AdminModerAuthorOrReadOnly
    ]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    serializer_class = ReviewSerializer

    def title_query(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.title_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_query())


class CommentViewSet(ReviewViewSet):
    """
    Разрешенные методы GET, POST, PATCH, DELETE.

    Права доступа: GET - Доступно без токена.
    POST - Аутентифицированные пользователи
    PATCH, DELETE - Автор, модер, админ
    """

    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        AdminModerAuthorOrReadOnly
    ]

    def review_query(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.review_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_query())
