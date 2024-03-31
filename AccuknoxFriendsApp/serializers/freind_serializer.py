from rest_framework import serializers
from ..models import FriendRequest


class FriendReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

    def update(self, instance, validated_data):
        if validated_data['is_accepted']:
            instance.is_accepted = True
        if validated_data['is_rejected']:
            instance.is_rejected = True
        instance.save()
        return instance
