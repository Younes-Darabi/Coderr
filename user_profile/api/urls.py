from django.urls import path

from .views import ProfileDetailView, BusinessListView, CustomerListView


urlpatterns = [
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('business/', BusinessListView.as_view(), name='profile-business'),
    path('customer/', CustomerListView.as_view(), name='profile-customer')
]