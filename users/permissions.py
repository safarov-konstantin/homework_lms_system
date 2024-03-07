from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    """
    Проверка для удаления и изменения
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj


class IsModerator(BasePermission):
    """
    Проверка принадлежности пользователя группе moderators
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='moderators').exists()
