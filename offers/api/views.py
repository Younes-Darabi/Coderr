from django.db.models import Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Offer, OfferDetail
from .serializers import OfferGetSerializer, OfferPostSerializer, SingleGetOfferSerializer, SinglePatchOfferSerializer, SingleOfferDetailSerializer
from .permissions import ISUserBusiness, IsOwner
from .paginations import OfferPagination


class OfferView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator_id']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    pagination_class = OfferPagination

    def get_queryset(self):
        queryset = Offer.objects.all()
        
        min_price = self.request.query_params.get('min_price')
        max_delivery_time = self.request.query_params.get('max_delivery_time')

        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(details__price__lte=min_price).distinct()
            except ValueError:
                pass

        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
                queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time)
            except ValueError:
                pass
            
        return queryset

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
    

class OfferDetailsView(generics.RetrieveAPIView):

    queryset = OfferDetail.objects.all()
    serializer_class = SingleOfferDetailSerializer
    permission_classes = [IsAuthenticated]