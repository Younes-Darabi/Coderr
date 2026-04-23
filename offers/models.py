from django.db import models

from user_auth.models import CustomUser


class Offer(models.Model):

    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField()
    creator = models.ForeignKey(
        CustomUser, related_name='offers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):

    class OfferType (models.TextChoices):
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    offer = models.ForeignKey(
        Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=30, choices=OfferType.choices)

    def __str__(self):
        return self.offer.title
