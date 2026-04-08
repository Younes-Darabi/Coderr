from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Offer
from .serializers import OfferGetSerializer, OfferPostSerializer, SingleGetOfferSerializer, SinglePatchOfferSerializer
from .permissions import ISUserBusiness, IsOwner
from .paginations import OfferPagination


class OfferView(generics.ListCreateAPIView):

    queryset = Offer.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['creator_id', 'min_price', 'max_delivery_time']
    filterset_fields = ['creator_id']
    search_fields = ['title', 'description']
    # ordering_fields = ['updated_at', 'min_price']
    ordering_fields = ['updated_at']

    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), ISUserBusiness()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferGetSerializer
        return OfferPostSerializer
    

class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SingleGetOfferSerializer
        return SinglePatchOfferSerializer