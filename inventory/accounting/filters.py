from django.contrib import admin
from django.db.models import Q
from inventory.common.models import *


class CompanylistFilter(admin.SimpleListFilter):
    title = 'Company'
    parameter_name = 'company'
    
    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(i.id, i.title) for i in Company.objects.all()]
        else:
            if request.user.is_owner and request.user.is_editor:
                queryset = CompanyUser.objects.filter(user=request.user)
                return [(i.company.id, i.company.title) for i in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(company_id=self.value())
        else:
            return queryset

class InventoryFilter(admin.SimpleListFilter):
    title = "Due"
    parameter_name = "Due"

    def lookups(self, request, model_admin):
        return [
            ("=0", "No Due"),
            (">0", "Has Due")
        ]

    def queryset(self, request, queryset):
        if self.value() == "=0":
            return queryset.filter(due=0)
        elif self.value() == ">0":
            return queryset.filter(Q(due__gt=0) | Q(account_type="DUE_PAY") | Q(account_type="DUE_RECEIVE"))


class CustomerlistFilter(admin.SimpleListFilter):
    title = 'Customer'
    parameter_name = 'customer'
    
    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(i.id, i.full_name) for i in Customer.objects.all()]
        else:
            if request.user.is_owner and request.user.is_editor:
                queryset1 = CompanyUser.objects.filter(user=request.user)
                queryset = Customer.objects.filter(company__in=[i.company.id for i in queryset1])
                return [(i.id, i.full_name) for i in queryset]
            
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(buyer_seller=self.value())
        else:
            return queryset


    

