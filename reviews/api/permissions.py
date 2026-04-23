from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    """
    Allows access only to users with 'customer' account type.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to allow only the reviewer to edit or delete their review.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.reviewer
