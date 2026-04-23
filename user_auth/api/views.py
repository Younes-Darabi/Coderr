from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    Handles new user registration and returns an authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                """ Save user and generate/retrieve token """
                saved_account = serializer.save()
                token, created = Token.objects.get_or_create(
                    user=saved_account)

                return Response({
                    'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email,
                    "user_id": saved_account.pk
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(ObtainAuthToken):
    """
    Authenticates a user and returns a token along with user details.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    "user_id": user.pk
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
