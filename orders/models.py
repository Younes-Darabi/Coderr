from django.db import models

from offers.models import OfferDetail
from user_auth.models import CustomUser


class Order(models.Model):

    class OrderStatus (models.TextChoices):
        IN_PROGRESS = "in_progress", "In_Progress"
        COMPLETED = "completed", "Completed"

    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE)
    customer_user = models.ForeignKey(CustomUser, related_name='user_as_customer', on_delete=models.CASCADE)
    business_user = models.ForeignKey(CustomUser, related_name='user_as_business', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)