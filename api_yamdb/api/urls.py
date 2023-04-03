from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (APIGetToken, CategoryViewSet, GenreViewSet,
                       APISignup, TitleViewSet, UserViewSet)

router = DefaultRouter()

router.register('categories', CategoryViewSet),
router.register('genres', GenreViewSet),
router.register('titles', TitleViewSet),
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('auth/signup/', APISignup.as_view(), name='signup'),
]
