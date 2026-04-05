from rest_framework import serializers

from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):

    offer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OfferDetail
        fields = ['offer', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True, required=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
