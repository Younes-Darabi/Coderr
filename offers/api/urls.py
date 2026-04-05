from django.urls import path
from .views import OfferView

urlpatterns = [
    path('', OfferView.as_view(), name='offer'),
]