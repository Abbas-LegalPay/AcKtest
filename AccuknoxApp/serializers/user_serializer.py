from rest_framework import serializers
from ..models import AccuKnoxUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccuKnoxUser
        # fields = "__all__"
        fields = ["email", "first_name", "last_name"]
