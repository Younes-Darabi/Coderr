from rest_framework import serializers

from ..models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user registration data and validation.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        pw = validated_data['password']
        repeated_pw = validated_data['repeated_password']

        # Ensure both passwords match
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': 'passwords dont match'})

        # Check for email uniqueness
        if CustomUser.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists'})

        # Create user instance and hash the password
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            type=validated_data.get('type', 'customer')
        )
        user.set_password(pw)
        user.save()
        return user
