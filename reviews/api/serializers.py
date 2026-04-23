from rest_framework import serializers

from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model, ensuring reviewer is managed automatically.
    """
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
