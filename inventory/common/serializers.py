from rest_framework.serializers import ModelSerializer
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.transaction import atomic
from .models import *

User = get_user_model()


class SimpleCustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CompanySerializer(ModelSerializer):
    company_type_name = serializers.SerializerMethodField(method_name="get_company_type_name")

    class Meta:
        model = Company
        fields = ["id", "title", "company_type", "company_type_name"]

    def get_company_type_name(self, obj):
        return obj.company_type.company_type

    def create(self, validated_data):
        user_id = self.context["user_id"]
        print(user_id)
        user = User.objects.get(pk=user_id)
        instance = Company.objects.create(
            owner=user,
            **validated_data
        )
        return instance


class CustomerTypeSerializer(ModelSerializer):
    class Meta:
        model = CustomerType
        fields = ["id", "customer_type"]


class CustomerSerializer(ModelSerializer):
    customer_type_name = serializers.SerializerMethodField(method_name="get_customer_type_name")

    class Meta:
        model = Customer
        fields = "__all__"
        include = ["customer_type_name"]

    def get_customer_type_name(self, obj):
        if obj:
            return obj.customer_type.customer_type
        return ""


class CreateCustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone", "address", "customer_type"]

    def create(self, validated_data):
        company_id = self.context["company_id"]
        company = Company.objects.get(pk=company_id)
        user_id = self.context["request"].user.id
        created_by = User.objects.get(pk=user_id)
        instance = Customer.objects.create(
            company=company,
            created_by=created_by,
            **validated_data
        )
        return instance


class UserPreferenceSerializer(ModelSerializer):
    company_name = serializers.SerializerMethodField(method_name="get_company_name")
    language_name = serializers.SerializerMethodField(method_name="get_language_name")
    currency_name = serializers.SerializerMethodField(method_name="get_currency_name")

    class Meta:
        model = UserPreference
        fields = ["company", "company_name", "language", "language_name", "currency", "currency_name"]

    def get_company_name(self, obj):
        return obj.company.title

    def get_language_name(self, obj):
        return obj.language.name

    def get_currency_name(self, obj):
        return obj.currency.name

    def create(self, validated_data):
        user_id = self.context["user_id"]
        user = User.objects.get(pk=user_id)
        instance = UserPreference.objects.create(
            user=user,
            **validated_data
        )
        return instance

    def update(self, instance, validated_data):
        instance = UserPreference.objects.filter(user=self.context["user_id"]).update(**validated_data)
        return instance


class DashboardCustomersSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "full_name", "email", "phone", "address"]


class CompanyTypeSerializer(ModelSerializer):
    company_type = serializers.SerializerMethodField(method_name="get_company_type")

    class Meta:
        model = CompanyType
        fields = "__all__"

    def get_company_type(self, obj):
        return obj.company_type.capitalize()


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class FAQSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Faqs)

    class Meta:
        model = Faqs
        fields = "__all__"


'''
class FAQSerializer(ModelSerializer):
    class Meta:
        model = Faqs
        fields = "__all__"
        '''


class EditorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password", "email", "first_name", "last_name",
                  "phone", "is_editor", "is_owner", "is_active", "is_staff", "groups"]

    def save(self, **kwargs):
        with atomic():
            user = User.objects.create(
                email=self.validated_data["email"],
                first_name=self.validated_data["first_name"],
                last_name=self.validated_data["last_name"],
                phone=self.validated_data["phone"],
                is_editor=self.validated_data["is_editor"],
                is_owner=self.validated_data["is_owner"],
                is_active=self.validated_data["is_active"],
                is_staff=self.validated_data["is_staff"],
                created_by=self.context["request"].user,
                password=make_password(self.validated_data["password"]),
            )
            for i in self.validated_data['groups']:
                user.groups.add(i.id)
            user.save()
            CompanyUser.objects.create(
                user=user,
                company=Company.objects.get(pk=self.context["company_id"])
            )
        return user


class UpdateEditorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password", "first_name", "last_name",
                  "phone", "is_editor", "is_owner", "is_active", "is_staff", "groups"]

    def update(self, instance, validated_data):
        with atomic():
            instance.first_name = validated_data["first_name"]
            instance.last_name = validated_data["last_name"]
            instance.phone = validated_data["phone"]
            instance.is_editor = validated_data["is_editor"]
            instance.is_owner = validated_data["is_owner"]
            instance.is_active = validated_data["is_active"]
            instance.is_staff = validated_data["is_staff"]
            if validated_data["password"]:
                instance.password = make_password(validated_data["password"])
            instance.groups.clear()
            for i in validated_data['groups']:
                instance.groups.add(i.id)
            instance.save()
        return instance
