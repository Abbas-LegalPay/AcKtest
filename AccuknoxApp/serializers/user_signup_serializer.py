from rest_framework import serializers
from ..models import AccuKnoxUser


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccuKnoxUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AccuKnoxUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
