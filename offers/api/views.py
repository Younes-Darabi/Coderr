from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import OfferSerializer
from ..models import Offer
from .permissions import ISUserBusiness


class OfferView(generics.ListCreateAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), ISUserBusiness()]