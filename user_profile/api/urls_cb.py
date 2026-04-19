from django.urls import path

from .views import BusinessListView, CustomerListView


urlpatterns = [
    path('business/', BusinessListView.as_view(), name='profile-business'),
    path('customer/', CustomerListView.as_view(), name='profile-customer')
]