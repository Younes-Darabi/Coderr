from rest_framework import permissions


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.reviewer
