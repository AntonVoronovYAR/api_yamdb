from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ на запись админу и суперюзеру, остальным read-only."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class AdminModerAuthorOrReadOnly(permissions.BasePermission):
    """Доступ автору, модератору, админу и суперюзеру."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        ))


class AdminOrSuperuser(permissions.BasePermission):
    """Доступ админу или суперюзеру."""

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )
