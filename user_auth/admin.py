from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'type', 'is_staff', 'date_joined']
    list_filter = ['type', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']


admin.site.register(CustomUser, UserAdmin)
