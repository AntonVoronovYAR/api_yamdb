from api.views import (
    APIGetToken, APISignup, CategoryViewSet, GenreViewSet,
    TitleViewSet, UserViewSet, ReviewViewSet, CommentViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet),
router_v1.register('genres', GenreViewSet),
router_v1.register('titles', TitleViewSet),
router_v1.register('users', UserViewSet),
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
auth_pattterns = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignup.as_view(), name='signup')
]
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_pattterns)),
]
