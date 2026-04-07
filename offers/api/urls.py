from django.urls import path
from .views import OfferView, SingleOfferView

urlpatterns = [
    path('', OfferView.as_view(), name='offer'),
    path('<int:pk>/', SingleOfferView.as_view(), name='offer-detail'),
]