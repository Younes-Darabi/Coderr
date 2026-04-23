from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import serializers

from ..models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomer, IsOwner


class ReviewView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomer()]

    def perform_create(self, serializer):
        business_user = serializer.validated_data['business_user']

        if Review.objects.filter(reviewer=self.request.user, business_user=business_user).exists():
            raise serializers.ValidationError(
                "You have already submitted a review for this business user.")

        serializer.save(reviewer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwner]
