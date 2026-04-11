from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

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