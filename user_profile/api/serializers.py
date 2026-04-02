from rest_framework import serializers
from user_auth.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source='id', read_only=True)
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at'
        ]


class BusinessListSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type'
        ]


class CustomerListSerializer(serializers.ModelSerializer):
    
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'type'
        ]