from rest_framework.serializers import ModelSerializer
from .models import Plan, Subscriber, PlanDetails
from rest_framework import serializers


class PlanDetailsSerializer(ModelSerializer):
    class Meta:
        model = PlanDetails
        fields = ["description"]


class PlanSerializer(ModelSerializer):
    plandetails_set = PlanDetailsSerializer(many=True)

    class Meta:
        model = Plan
        fields = [
            "id",
            "title",
            "price",
            "discount",
            "duration",
            "plandetails_set",
            "active",
            "created_at"
        ]


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = [
            "id",
            "plan",
            "user",
            "active",
            "created_at"
        ]
