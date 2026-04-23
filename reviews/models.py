from django.db import models

from user_auth.models import CustomUser


class Review(models.Model):

    reviewer = models.ForeignKey(
        CustomUser, related_name='reviewer_as_customer', on_delete=models.CASCADE)
    business_user = models.ForeignKey(
        CustomUser, related_name='business_user_as_business', on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
