from django.db import models


class Offer(models.Model):

    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class OfferDetail(models.Model):

    class OfferType (models.TextChoices):
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=30, choices=OfferType.choices)

    def __str__(self):
        return self.offer.title