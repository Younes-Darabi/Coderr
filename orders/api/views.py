from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from offers.models import OfferDetail
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomer

class OrderView(generics.ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomer()]
    
    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get('offer_detail_id')

        if not offer_detail_id:
            return Response({"detail": "The fields are incomplete."}, status=status.HTTP_400_BAD_REQUEST)
        
        offer_detail = get_object_or_404(OfferDetail, id=offer_detail_id)
        data={
            "customer_user": request.user.id,
            "business_user": offer_detail.offer.creator.id,
             "offer_detail":  offer_detail.id
        }
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response (serializer.errors,  status=status.HTTP_400_BAD_REQUEST)