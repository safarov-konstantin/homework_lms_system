from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Проверка принадлежат данные пользователю
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user == view.get_object().owner


class IsModerator(BasePermission):
    """
    Проверка принадлежности пользователя группе moderators
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='moderators').exists()
