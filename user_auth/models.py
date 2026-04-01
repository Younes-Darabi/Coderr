from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS_USER = "business-user", "Business-User"
    
    type = models.CharField(max_length=20, choices=UserType.choices)

    def __str__(self):
        return self.username