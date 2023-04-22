from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owner to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrIsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owner or admin to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
