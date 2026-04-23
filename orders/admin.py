from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'offer_detail', 'customer_user',
                    'business_user', 'status', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['offer_detail',
                     'customer_user', 'business_user', 'status']
    ordering = ['-created_at']


admin.site.register(Order, OrderAdmin)
