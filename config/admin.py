from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from inventory.subscription.models import *
from inventory.common.models import *


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        global subscriber
        subscriber = False
        try:
            subscriber = Subscriber.objects.filter(user=Company.objects.filter(
                pk=CompanyUser.objects.filter(user=user.id).first().company.id).first().owner).first().active
        except:
            pass
        if not subscriber and not user.is_superuser:
            raise ValidationError(
                RegexValidator(message='Subscription expired. Please renew your subscription.').message,
            )

        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


admin.AdminSite.login_form = CustomAuthenticationForm


class MyAdminSite(admin.AdminSite):
    pass
