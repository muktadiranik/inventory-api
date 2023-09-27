from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.contrib.auth import get_user_model
from inventory.accounting.filters import *
from django.db.models import Q
from .models import *

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)

User = get_user_model()


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ("name",)
    ordering = ('id',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ("name", )
    ordering = ('id',)


@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('customer_type',)
    search_fields = ('customer_type',)
    ordering = ('id',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
        'email',
        'company',
        'customer_type',
        'address',
        'created_at',
        'created_by',
    )
    list_display_links = ["full_name"]

    search_fields = (
        'full_name',
        'email',
        'phone',
        "company__owner__email",
    )

    list_filter = (CompanylistFilter, 'customer_type',)
    fields = (
        'first_name',
        'last_name',
        'phone',
        'email',
        'company',
        'customer_type',
        'address',
        'created_by',
    )

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
            if db_field.name == "created_by":
                kwargs["queryset"] = User.objects.filter(is_superuser=False)
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


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('company_type',)
    search_fields = ('company_type',)
    ordering = ('id',)


class CompanyUserAdmin(admin.StackedInline):
    model = CompanyUser

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
            if db_field.name == "user":
                kwargs["queryset"] = User.objects.filter(is_superuser=False)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company)
            if db_field.name == "user":
                if request.user.is_superuser:
                    kwargs["queryset"] = User.objects.filter(
                        is_superuser=False)
                company = Company.objects.filter(owner=request.user)
                company_user = CompanyUser.objects.filter(company__in=company)
                kwargs["queryset"] = User.objects.filter(
                    Q(created_by=request.user) | Q(pk__in=[i.user.id for i in company_user]))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'company_type')
    search_fields = ('title', "owner__email")
    list_filter = ('company_type',)
    inlines = [CompanyUserAdmin]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            if db_field.name == "owner":
                kwargs["queryset"] = User.objects.filter(is_superuser=False)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "owner":
                kwargs["queryset"] = User.objects.filter(email=request.user)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    search_fields = ('user__email', 'company__title')
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
            if db_field.name == "user":
                kwargs["queryset"] = User.objects.filter(is_superuser=False)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company)
            if db_field.name == "user":
                kwargs["queryset"] = User.objects.filter(
                    created_by=request.user)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'language', 'currency')
    search_fields = ('user__email', 'company__title')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "company":
                if request.user.is_owner:
                    queryset = CompanyUser.objects.filter(user=request.user)
                    kwargs["queryset"] = Company.objects.filter(
                        pk__in=[i.company.id for i in queryset])
                else:
                    kwargs["queryset"] = Company.objects.filter(
                        pk=UserPreference.objects.get(user=request.user).company)
            if db_field.name == "user":
                kwargs["queryset"] = User.objects.filter(
                    created_by=request.user)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FaqAdmin(TranslatableAdmin):
    list_display = ["question", "answer", "created_at"]

    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
    )



'''
class FaqAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "created_at"]

'''
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)
admin.site.register(Faqs, FaqAdmin)
# admin.site.register(FAQ, FaqAdmin)


'''
    Unregistering the default django-celery-beat admin

    from django_celery_beat.models import (
        IntervalSchedule,
        CrontabSchedule,
        SolarSchedule,
        ClockedSchedule,
        PeriodicTask,
    )

'''


admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
