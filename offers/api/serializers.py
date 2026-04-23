from rest_framework import serializers

from user_auth.models import CustomUser
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Basic serializer for offer details."""
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer that provides custom URLs for offer details."""
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class UserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for basic user information attached to an offer."""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']


class OfferGetSerializer(serializers.ModelSerializer):
    """Serializer for listing offers with aggregated data like min_price."""
    user = serializers.IntegerField(source='creator_id', read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        return min(obj.details.all().values_list('price', flat=True))

    def get_min_delivery_time(self, obj):
        return min(obj.details.all().values_list('delivery_time_in_days', flat=True))


class OfferPostSerializer(serializers.ModelSerializer):
    """Serializer for creating an offer along with its multiple details."""
    details = OfferDetailSerializer(many=True, required=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(creator=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class SingleGetOfferSerializer(serializers.ModelSerializer):
    """Serializer for detailed retrieval of a single offer."""
    user = serializers.IntegerField(source='creator_id', read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time']

    def get_min_price(self, obj):
        return min(obj.details.all().values_list('price', flat=True))

    def get_min_delivery_time(self, obj):
        return min(obj.details.all().values_list('delivery_time_in_days', flat=True))


class SingleOfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']


class SinglePatchOfferSerializer(serializers.ModelSerializer):
    """Handles updating an offer and its corresponding details (tiers)."""
    details = SingleOfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):

        details_data = validated_data.pop('details', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        for data in details_data:
            offer_type = data.get('offer_type')

            if offer_type is None:
                raise serializers.ValidationError({
                    "details": "Each detail must include 'offer_type'."
                })

            detail_obj, created = OfferDetail.objects.update_or_create(
                offer=instance,
                offer_type=offer_type,
                defaults=data
            )

        return instance
