from rest_framework import serializers
from .models import Group
from django.contrib.auth import get_user_model


User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group

        fields = [
            "id",
            "name",
            "description",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "created_at"
        ]


class AddMemberSerializer(serializers.Serializer):

    email = serializers.EmailField()

