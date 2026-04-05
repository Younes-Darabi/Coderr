from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import OfferSerializer
from ..models import Offer


class OfferView(generics.ListCreateAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]