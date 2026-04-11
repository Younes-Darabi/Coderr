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
    title = models.CharField(max_length=200)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=OrderStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"Order {self.id} - {self.offer_detail.title} - {self.customer_user.id} - {self.business_user.id}"