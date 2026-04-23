from rest_framework import generics, filters, serializers
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomer, IsOwner


class ReviewView(generics.ListCreateAPIView):
    """
    List all reviews with filtering/ordering or create a new review.
    A customer can only review a business once.
    """
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """ GET is allowed for all authenticated users; POST only for customers. """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomer()]

    def perform_create(self, serializer):
        """
        Customizes the creation logic to check if a review already exists 
        from the current reviewer for the target business user.
        """
        business_user = serializer.validated_data['business_user']

        if Review.objects.filter(reviewer=self.request.user, business_user=business_user).exists():
            raise serializers.ValidationError(
                "You have already submitted a review for this business user.")

        serializer.save(reviewer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific review.
    Updates and Deletions are restricted to the review owner.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwner]
