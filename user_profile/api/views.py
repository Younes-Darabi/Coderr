from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from user_auth.models import CustomUser
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]