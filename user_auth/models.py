from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model to distinguish between customers and business users,
    and to store additional profile information.
    """
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    # User role identification
    type = models.CharField(max_length=20, choices=UserType.choices)

    # Profile information fields
    file = models.FileField(upload_to='profile_files/', blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update 'uploaded_at' timestamp 
        whenever a new file is uploaded.
        """
        if self.file:
            self.uploaded_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
