from rest_framework import serializers

from user_auth.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user profiles, including full contact 
    and description fields. Maps 'id' to 'user' for API consistency.
    """
    user = serializers.IntegerField(source='id', read_only=True)
    created_at = serializers.DateTimeField(
        source='date_joined', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'location',
            'tel', 'description', 'working_hours', 'type', 'email', 'created_at'
        ]


class BusinessListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing business profiles.
    Excludes private data like email and exact join dates.
    """
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'location',
            'tel', 'description', 'working_hours', 'type'
        ]


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing customer profiles.
    Focuses on basic identification and file upload information.
    """
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type'
        ]
