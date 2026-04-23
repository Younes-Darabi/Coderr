from rest_framework import permissions


class ISUserBusiness(permissions.BasePermission):
    """Permission to check if the user is registered as a business."""

    def has_permission(self, request, view):
        return request.user.type == 'business'


class IsOwner(permissions.BasePermission):
    """Permission to check if the user is the creator of the offer."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
