from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Offer, OfferDetail
from .serializers import (
    OfferGetSerializer, OfferPostSerializer, SingleGetOfferSerializer,
    SinglePatchOfferSerializer, SingleOfferDetailSerializer
)
from .permissions import ISUserBusiness, IsOwner
from .paginations import OfferPagination


class OfferView(generics.ListCreateAPIView):
    """
    Handles listing offers with filtering/sorting and creating new offers.
    GET: Public access. POST: Restricted to business users.
    """
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator_id']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    pagination_class = OfferPagination

    def get_queryset(self):
        """
        Customizes the queryset to support filtering by min_price and max_delivery_time.
        """
        queryset = Offer.objects.all()
        min_price_param = self.request.query_params.get('min_price')
        max_delivery_time_param = self.request.query_params.get(
            'max_delivery_time')

        if min_price_param:
            try:
                min_price_param = float(min_price_param)
                queryset = queryset.annotate(
                    min_detail_price=Min('details__price'))
                queryset = queryset.filter(
                    min_detail_price__gte=min_price_param)
            except ValueError:
                raise serializers.ValidationError(
                    "You must enter a number for the minimum price filter.")

        if max_delivery_time_param:
            try:
                max_delivery_time_param = int(max_delivery_time_param)
                queryset = queryset.filter(
                    details__delivery_time_in_days__lte=max_delivery_time_param).distinct()
            except ValueError:
                raise serializers.ValidationError(
                    "You must enter a number for the maximum delivery time filter.")
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
    """
    Handles detailed retrieval, updating, and deletion of a specific offer.
    Updating and Deleting are restricted to the owner.
    """
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
    """
    Retrieves details for a specific pricing tier (OfferDetail).
    """
    queryset = OfferDetail.objects.all()
    serializer_class = SingleOfferDetailSerializer
    permission_classes = [IsAuthenticated]
