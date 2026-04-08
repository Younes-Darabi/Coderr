from rest_framework import serializers

from ..models import Offer, OfferDetail
from user_auth.models import CustomUser

class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='offer-detail', read_only=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']


class OfferGetSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source = 'creator_id', read_only = True)
    details = OfferDetailHyperlinkedSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='creator',read_only = True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
    
    def get_min_price(self, obj):
        return min(obj.details.all().values_list('price', flat=True))

    def get_min_delivery_time(self, obj):
        return min(obj.details.all().values_list('delivery_time_in_days', flat=True))



class OfferPostSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True, required=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def create(self, validated_data):

        details_data = validated_data.pop('details')
        user = self.context['request'].user
        
        offer = Offer.objects.create(creator=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    

class SingleOfferSerializer(serializers.ModelSerializer):
    pass