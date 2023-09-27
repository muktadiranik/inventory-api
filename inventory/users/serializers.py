from django.contrib.auth import authenticate
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions
from django.contrib.auth.models import Group
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.utils import email_address_exists
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')
from django.db.transaction import atomic
from inventory.subscription.models import *
from inventory.common.models import *
from inventory.common.validators import *
from inventory.subscription.models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import exceptions as url_exceptions
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers


User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    def _validate_email(self, email, password):
        global subscriber
        subscriber = False
        try:
            user = User.objects.get(email=email)
            subscriber = Subscriber.objects.filter(user=Company.objects.filter(
                pk=CompanyUser.objects.filter(user=user.id).first().company.id).first().owner).first().active
        except:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)
        if not subscriber:
            msg = _('Subscription expired. Please renew your subscription.')
            raise exceptions.ValidationError(msg)
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user(self, username, email, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if 'allauth' in settings.INSTALLED_APPS:
            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password)
            except url_exceptions.NoReverseMatch:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, password)


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, validators=[alphanumeric])
    last_name = serializers.CharField(required=True, validators=[alphanumeric])
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, read_only=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, validators=[phone_regex, MinLengthValidator(11)])
    is_owner = serializers.BooleanField(required=True)
    is_editor = serializers.BooleanField(required=True)
    # add user to groups
    groups = serializers.ManyRelatedField(child_relation=serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()), required=False)
    # add a plan field to the serializer
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), required=False)
    # add a company field to the serializer
    company_title = serializers.CharField(required=False)
    company_type = serializers.PrimaryKeyRelatedField(
        queryset=CompanyType.objects.all(), required=False)
    # user preferences
    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), required=False)
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), required=False)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'is_owner': self.validated_data.get('is_owner', ''),
            'is_editor': self.validated_data.get('is_editor', ''),
            "plan": self.validated_data.get("plan", ""),
            "company_title": self.validated_data.get("company_title", ""),
            "company_type": self.validated_data.get("company_type", ""),
            "language": self.validated_data.get("language", ""),
            "currency": self.validated_data.get("currency", ""),
        }

    def save(self, request):
        with atomic():
            adapter = get_adapter()
            user = adapter.new_user(request)
            self.cleaned_data = self.get_cleaned_data()
            user = adapter.save_user(request, user, self, commit=False)
            if "password1" in self.cleaned_data:
                try:
                    adapter.clean_password(self.cleaned_data['password1'], user=user)
                except DjangoValidationError as exc:
                    raise serializers.ValidationError(
                        detail=serializers.as_serializer_error(exc)
                    )
            user.is_owner = self.cleaned_data.get('is_owner')
            user.is_editor = self.cleaned_data.get('is_editor')
            user.phone = self.cleaned_data.get('phone')
            user.created_by = None
            user.save()
            # add user to groups
            for i in Group.objects.all():
                user.groups.add(i.id)
            self.custom_signup(request, user)
            setup_user_email(request, user, [])
            # add a company of the user
            company_type_id = self.cleaned_data.get("company_type")
            company_type = CompanyType.objects.get(id=company_type_id.id)
            company_instance = Company.objects.create(
                title=self.cleaned_data.get("company_title"),
                company_type=company_type,
                owner=user
            )
            # add user as a subscriber
            Subscriber.objects.create(
                user=user,
                plan_id=self.cleaned_data.get("plan").id,
                active=True
            )
            # add a relation of company and user
            """
            CompanyUser.objects.create(
                user=user,
                company=company_instance,
            )
            """
            # user preferences
            UserPreference.objects.create(
                user=user,
                company=company_instance,
                language=Language.objects.get(pk=self.cleaned_data.get("language").id),
                currency=Currency.objects.get(pk=self.cleaned_data.get("currency").id),
            )
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'phone', 'is_owner', 'is_editor')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_owner = validated_data.get('is_owner', instance.is_owner)
        instance.is_editor = validated_data.get('is_editor', instance.is_editor)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
