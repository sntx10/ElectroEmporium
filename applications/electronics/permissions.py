from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsSellerOrReadOnly(permissions.BasePermission):
    # CREATE, LIST
    def has_permission(self, request, view):
        """
        Только авторизованный продавец может добавлять продукты
        """
        if request.method == 'GET':
            return True
        try:
            return request.user.is_seller and request.user.is_authenticated
        except AttributeError:
            return False

    # RETRIEVE, UPDATE, DELETE
    def has_object_permission(self, request, view, obj):
        """
        Только авторизованный продавец и владелец товара может его изменять или удалять
        """
        if request.method in SAFE_METHODS:
            return True
        try:
            return request.user.is_authenticated and (
                    (request.user == obj.user and request.user.is_seller) or request.user.is_staff)
        except AttributeError:
            return False
