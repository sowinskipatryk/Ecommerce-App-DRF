from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_seller
        return False


class IsClient(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_client
        return False
