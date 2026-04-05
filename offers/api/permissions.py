from rest_framework import permissions


class ISUserBusiness(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.type == 'business-user'