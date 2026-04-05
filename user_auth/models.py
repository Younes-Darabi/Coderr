from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS_USER = "business-user", "Business-User"
    
    type = models.CharField(max_length=20, choices=UserType.choices)
    file = models.FileField(upload_to='profile_files/', blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")

    def save(self, *args, **kwargs):
        if self.file:
            self.uploaded_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username