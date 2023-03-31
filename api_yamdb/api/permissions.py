from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    '''
    Доступ на запись админу и суперюзеру, остальным read-only.
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                if request.user.is_admin:
                    return True



class AdminModerAuthorOrReadOnly(permissions.BasePermission):
    '''
    Доступ автору, модератору, админу и суперюзеру.
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return (user == obj.author or user.is_moderator)


class AdminOrSuperuser(permissions.BasePermission):
    '''
    Доступ админу или суперюзеру.
    '''

    def has_permission(self, request, view):
        return getattr(request.user, 'is_admin', False)


class AuthorOrAuthenticated(permissions.BasePermission):
    '''
    Право на просмотр аутентифицированным пользователям,
    и право на запись автору.
    '''

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
