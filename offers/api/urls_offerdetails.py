from django.urls import path
from .views import OfferDetailsView

urlpatterns = [
    path('<int:pk>/', OfferDetailsView.as_view(), name='offer-details'),
]