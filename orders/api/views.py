from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import Response, APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from offers.models import OfferDetail
from user_auth.models import CustomUser
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomer, IsBusiness


class OrderView(generics.ListCreateAPIView):
    """
    Handles listing all orders and creating new ones.
    Creation is restricted to customers.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Only authenticated customers can place new orders
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomer()]

    def create(self, request, *args, **kwargs):
        """
        Custom create method to automatically link the customer (current user) 
        and the business user (creator of the offer tier).
        """
        offer_detail_id = request.data.get('offer_detail_id')

        if not offer_detail_id:
            return Response({"detail": "The fields are incomplete."}, status=status.HTTP_400_BAD_REQUEST)

        offer_detail = get_object_or_404(OfferDetail, id=offer_detail_id)

        # Prepare data for the serializer
        data = {
            "customer_user": request.user.id,
            "business_user": offer_detail.offer.creator.id,
            "offer_detail":  offer_detail.id
        }
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles individual order operations. 
    Status updates (PATCH) are restricted to business users.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Business users can update order status (e.g., mark as completed)
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusiness()]
        return [IsAuthenticated(), IsAdminUser()]


class OrderCountView(APIView):
    """
    Returns the count of 'in_progress' orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        business_user = get_object_or_404(CustomUser, id=pk)
        order_count = Order.objects.filter(
            business_user=business_user, status='in_progress').count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    Returns the count of 'completed' orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        business_user = get_object_or_404(CustomUser, id=pk)
        completed_order_count = Order.objects.filter(
            business_user=business_user, status='completed').count()
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)
