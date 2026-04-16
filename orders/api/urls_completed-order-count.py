from django.urls import path
from .views import CompletedOrderCountView

urlpatterns = [
    path('<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count')
]