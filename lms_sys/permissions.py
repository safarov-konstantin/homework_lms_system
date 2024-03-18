from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Проверка принадлежат данные пользователю
    """
    # def has_permission(self, request, view):
    #     if request.user.is_superuser:
    #         return True
    #     a = request.user
    #     c = view.get_object()
    #     b = view.get_object().owner
    #     return request.user == view.get_object().owner

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.owner == request.user
