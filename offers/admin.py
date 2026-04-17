from django.contrib import admin

from .models import Offer


class OfferAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'creator', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    ordering = ['-created_at']


admin.site.register(Offer, OfferAdmin)
