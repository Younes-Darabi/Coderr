from rest_framework import permissions


class ISUserBusiness(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type == 'business'


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
