from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_auth.api.urls')),
    path('api/profile/', include('user_profile.api.urls')),
    path('api/profiles/', include('user_profile.api.urls_cb')),
    path('api/offers/', include('offers.api.urls')),
    path('api/offerdetails/', include('offers.api.urls_offerdetails')),
    path('offerdetails/', include('offers.api.urls_offerdetails')),
    path('api/orders/', include('orders.api.urls')),
    path('api/order-count/', include('orders.api.urls_order-count')),
    path('api/completed-order-count/', include('orders.api.urls_completed-order-count')),
    path('api/reviews/', include('reviews.api.urls')),
    path('api/base-info/', include('base_info.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)