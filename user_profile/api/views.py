from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user_auth.models import CustomUser
from .serializers import ProfileSerializer, BusinessListSerializer, CustomerListSerializer
from .permissions import IsOwner


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint to retrieve or update a specific user profile.
    Supports GET (Retrieve) and PATCH (Partial Update).
    """
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        PATCH requests require the user to be the owner of the profile.
        """
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class BusinessListView(generics.ListAPIView):
    """
    Endpoint to retrieve a list of all users registered as 'business'.
    """
    queryset = CustomUser.objects.filter(type='business')
    serializer_class = BusinessListSerializer
    permission_classes = [IsAuthenticated]


class CustomerListView(generics.ListAPIView):
    """
    Endpoint to retrieve a list of all users registered as 'customer'.
    """
    queryset = CustomUser.objects.filter(type='customer')
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated]
