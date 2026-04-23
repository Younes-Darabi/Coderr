from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):

    list_display = ['id', 'created_at', 'reviewer', 'business_user']
    list_filter = ['created_at']
    search_fields = ['reviewer', 'business_user']
    ordering = ['-created_at']


admin.site.register(Review, ReviewAdmin)
