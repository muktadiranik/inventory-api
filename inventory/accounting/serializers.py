from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db.models.aggregates import Sum
from .models import *
from inventory.common.models import *
from inventory.common.serializers import *


class DashboardTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["total_balance", "cash_in_hand", "total_receivable", "total_payable", "profit_loss"]


class ChartOfAccountSerializer(ModelSerializer):
    class Meta:
        model = ChartOfAccount
        fields = ["id", "name", "value", "parent", "description"]


class PlotSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    category_name = serializers.CharField(source="category.name", required=False, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["company", "category_name"]

    def create(self, validated_data):
        company_id = self.context["company_id"]
        print(company_id)
        company = Company.objects.get(pk=company_id)
        validated_data["company"] = company
        return super().create(validated_data)


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"
        read_only_fields = ["company"]

    def create(self, validated_data):
        company_id = self.context["company_id"]
        company = Company.objects.get(pk=company_id)
        validated_data["company"] = company
        return super().create(validated_data)


class CreateTransactionSerializer(ModelSerializer):
    created_at = serializers.ReadOnlyField()
    income_expense = serializers.ReadOnlyField()
    due = serializers.ReadOnlyField()
    cash_in_hand = serializers.ReadOnlyField()
    total_receivable = serializers.ReadOnlyField()
    total_payable = serializers.ReadOnlyField()
    total_balance = serializers.ReadOnlyField()
    profit_loss = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = ["id", "created_at", "buyer_seller", "product", "description", "quantity", "unit_price", "account_type",
                  "income_expense", "paid_amount", "due", "total_balance", "cash_in_hand", "total_receivable", "total_payable", "profit_loss"]

    def create(self, validated_data):
        company_id = self.context["company_id"]
        company = Company.objects.get(pk=company_id)
        validated_data["company"] = company
        return super().create(validated_data)


class TransactionSerializer(ModelSerializer):
    created_at = serializers.ReadOnlyField()
    income_expense = serializers.ReadOnlyField()
    due = serializers.ReadOnlyField()
    cash_in_hand = serializers.ReadOnlyField()
    total_receivable = serializers.ReadOnlyField()
    total_payable = serializers.ReadOnlyField()
    total_balance = serializers.ReadOnlyField()
    profit_loss = serializers.ReadOnlyField()
    buyer_seller = CustomerSerializer(read_only=True)
    buyer_seller_name = serializers.SerializerMethodField(method_name="get_buyer_seller_name", required=False)
    buyer_seller_id = serializers.SerializerMethodField(method_name="get_buyer_seller_id", required=False)
    product = ProductSerializer(read_only=True)
    product_name = serializers.SerializerMethodField(method_name="get_product_name", required=False)
    custom_description = serializers.SerializerMethodField(method_name="get_custom_description", required=False)

    class Meta:
        model = Transaction
        fields = ["id", "created_at", "buyer_seller", "product", "description",
                  "quantity", "unit_price", "account_type",
                  "income_expense", "paid_amount", "due", "total_balance",
                  "cash_in_hand", "total_receivable", "total_payable",
                  "profit_loss", "buyer_seller_id", "buyer_seller_name",
                  "product_name", "custom_description"]

    def get_buyer_seller_id(self, obj):
        if obj.buyer_seller is not None:
            return obj.buyer_seller.id
        return "-"

    def get_buyer_seller_name(self, obj):
        if obj.buyer_seller is not None:
            return obj.buyer_seller.full_name
        return "-"

    def get_product_name(self, obj):
        if obj.product is not None:
            return obj.product.name
        return "-"

    def get_custom_description(self, obj):
        if len(obj.description) > 0:
            return obj.description
        return "-"


class ProfiteLossSerializer(ModelSerializer):
    total_income = serializers.SerializerMethodField(method_name="get_total_income")
    total_expense = serializers.SerializerMethodField(method_name="get_total_expense")
    profite_or_loss = serializers.SerializerMethodField(method_name="get_profite_or_loss")
    is_profite_or_loss = serializers.SerializerMethodField(method_name="get_is_profite_or_loss")

    class Meta:
        model = Company
        fields = ["total_income", "total_expense", "profite_or_loss", "is_profite_or_loss"]

    def get_total_income(self, obj):
        return obj.transaction_set.filter(account_type="INCOME").aggregate(total_income=Sum("income_expense"))

    def get_total_expense(self, obj):
        return obj.transaction_set.filter(account_type="EXPENSE").aggregate(total_expense=Sum("income_expense"))

    def get_profite_or_loss(self, obj):
        total_income = obj.transaction_set.filter(account_type="INCOME").aggregate(total_income=Sum("income_expense"))
        total_expense = obj.transaction_set.filter(
            account_type="EXPENSE").aggregate(total_expense=Sum("income_expense"))
        return total_income["total_income"] - total_expense["total_expense"]

    def get_is_profite_or_loss(self, obj):
        total_income = obj.transaction_set.filter(account_type="INCOME").aggregate(total_income=Sum("income_expense"))
        total_expense = obj.transaction_set.filter(
            account_type="EXPENSE").aggregate(total_expense=Sum("income_expense"))
        if total_income["total_income"] > total_expense["total_expense"]:
            return "Profite"
        else:
            return "Loss"
