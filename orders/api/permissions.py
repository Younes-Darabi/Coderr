from rest_framework import permissions


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsBusiness(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'business'
