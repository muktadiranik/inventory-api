from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import *
from .models import *


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.prefetch_related("plandetails_set").all()
    search_fields = ["title"]
    http_method_names = ["get"]
    permission_classes = [permissions.AllowAny]


class SubscriberViewSet(ModelViewSet):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
    http_method_names = ["get", "post"]
