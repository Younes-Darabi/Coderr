from rest_framework import serializers

from ..models import Order
from offers.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model. 
    Automatically flattens details from the related OfferDetail for the response.
    """
    offer_detail = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(), write_only=True)

    # Read-only fields derived from the selected offer tier
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(
        source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(
        source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.IntegerField(
        source='offer_detail.price', read_only=True)
    features = serializers.JSONField(
        source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(
        source='offer_detail.offer_type', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'offer_detail', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at'
        ]
