from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       UserViewSet)

router = DefaultRouter()

router.register('categories', CategoryViewSet),
router.register('genres', GenreViewSet),
router.register('titles', TitleViewSet),
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
