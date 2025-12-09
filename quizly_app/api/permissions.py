from rest_framework import permissions


class IsOwnerAndAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit the Quiz.
    """
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.owner == request.user