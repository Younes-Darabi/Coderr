from rest_framework.views import APIView, Response
from django.db.models import Avg
from rest_framework.permissions import AllowAny

from reviews.models import Review
from user_auth.models import CustomUser
from offers.models import Offer


class BaseInfoView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        review_count = Review.objects.all().count()
        average_rating = Review.objects.aggregate(Avg("rating"))['rating__avg']
        business_profile_count =  CustomUser.objects.filter(type='business-user').count()
        offer_count = Offer.objects.all().count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }

        return Response(data=data)