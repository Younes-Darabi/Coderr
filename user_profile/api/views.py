from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user_auth.models import CustomUser
from .serializers import ProfileSerializer, BusinessListSerializer, CustomerListSerializer
from .permissions import IsOwner


class ProfileDetailView(generics.RetrieveUpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class BusinessListView(generics.ListAPIView):

    queryset = CustomUser.objects.filter(type='business')
    serializer_class = BusinessListSerializer
    permission_classes = [IsAuthenticated]


class CustomerListView(generics.ListAPIView):

    queryset = CustomUser.objects.filter(type='customer')
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated]
