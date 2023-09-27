from django.contrib.auth import get_user_model
from rest_framework import serializers
from inventory.common.models import *
from inventory.common.serializers import *

User = get_user_model()


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone",
                  "is_owner", "is_editor", "company_set", "image"]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password", "first_name", "last_name", "phone",
                  "is_owner", "is_editor", "image"]
