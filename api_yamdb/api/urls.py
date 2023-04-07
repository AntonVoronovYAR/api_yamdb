from api.views import (
    APIGetToken, APISignup, CategoryViewSet, GenreViewSet,
    TitleViewSet, UserViewSet, ReviewViewSet, CommentViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories', CategoryViewSet),
router.register('genres', GenreViewSet),
router.register('titles', TitleViewSet),
router.register('users', UserViewSet),
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('auth/signup/', APISignup.as_view(), name='signup'),
]
