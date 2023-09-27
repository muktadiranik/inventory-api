from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriptionConfig(AppConfig):
    name = 'inventory.subscription'
    verbose_name = _("Subscriptions")
