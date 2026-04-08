from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_auth.api.urls')),
    path('api/profile/', include('user_profile.api.urls')),
    path('api/offers/', include('offers.api.urls')),
    path('api/offerdetails/', include('offers.api.urls_offerdetails'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)