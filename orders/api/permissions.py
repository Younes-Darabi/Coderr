from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    """Checks if the user is authenticated and registered as a customer."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsBusiness(permissions.BasePermission):
    """Checks if the user is authenticated and registered as a business user."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'business'
