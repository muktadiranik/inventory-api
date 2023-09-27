from django.contrib import admin
from django.db.models import Q
from . models import Transaction, Product, ProductCategory, ChartOfAccount
from .forms import *
from import_export.admin import ImportExportModelAdmin
from inventory.common.models import *
from .filters import *


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'unit',
        "stock",
        'category',
        'description',
        "company",
    )
    search_fields = ('name', 'category__name')
    list_filter = (CompanylistFilter,)
    list_per_page = 20
    form = ProductModelForm

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner and request.user.is_editor:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company.id)

            if db_field.name == "category":
                kwargs["queryset"] = ProductCategory.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',)
    search_fields = ('name', 'company__title')
    list_filter = (CompanylistFilter,)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner and request.user.is_editor:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TransactionAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "company",
        "buyer_seller",
        "product",
        "description",
        "quantity",
        "unit_price",
        "account_type",
        "income_expense",
        "paid_amount",
        "due",
        "total_balance",
        "cash_in_hand",
        "total_receivable",
        "total_payable",
        "profit_loss",
    ]

    list_display_links = ["buyer_seller", "account_type"]
    list_filter = [CompanylistFilter, InventoryFilter,
                   CustomerlistFilter, "account_type", ]
    search_fields = ["buyer_seller__full_name",
                     "product__name", "company__owner__email"]
    list_per_page = 100
    fields = ["company", "buyer_seller", "product", "description",
              "quantity", "unit_price", "account_type", "paid_amount"]
    form = TransactionModelForm

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner and request.user.is_editor:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company.id)

            if db_field.name == "buyer_seller":
                kwargs["queryset"] = Customer.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            if db_field.name == "product":
                kwargs["queryset"] = Product.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ChartOfAccountAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "value",
        "parent",
        "description",
        "company",
    ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return ChartOfAccount.objects.filter(company__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner and request.user.is_editor:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company.id)

            if db_field.name == "parent":
                kwargs["queryset"] = ChartOfAccount.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            return super().formfield_for_foreignkey(db_field, request, **kwargs)




# admin.site.register(ChartOfAccount, ChartOfAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
