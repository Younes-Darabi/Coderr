from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Checks if the object's primary key matches the requesting user's ID.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are handled by the view,
        # this specifically checks if the user is the 'owner' of the profile
        return obj.pk == request.user.pk
