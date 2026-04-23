from rest_framework.views import APIView, Response
from django.db.models import Avg
from rest_framework.permissions import AllowAny

from reviews.models import Review
from user_auth.models import CustomUser
from offers.models import Offer


class BaseInfoView(APIView):
    """
    Public endpoint to provide platform-wide statistics.
    Calculates total reviews, average ratings, business user count, and total offers.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Counting total reviews across the platform
        review_count = Review.objects.all().count()

        # Calculating the average rating using Django's aggregate function
        average_rating = Review.objects.aggregate(Avg("rating"))['rating__avg']

        # Counting only users registered as 'business'
        business_profile_count = CustomUser.objects.filter(
            type='business').count()

        # Counting all available service offers
        offer_count = Offer.objects.all().count()

        data = {
            "review_count": review_count,
            # Handle None if no reviews exist
            "average_rating": average_rating if average_rating else 0,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }

        return Response(data=data)
