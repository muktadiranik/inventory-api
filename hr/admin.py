from django.contrib import admin
from django.db.models import Q
from inventory.accounting.filters import CompanylistFilter
from inventory.common.models import *
from .models import *
from .forms import *
from .filters import *


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'address', 'city', 'state', 'country',
                    'zip_code', 'department', 'job_title', 'salary', 'resume', 'date_of_joining', 'company']
    exclude = ('full_name',)
    list_filter = [JobTitlelistFilter, CompanylistFilter, ]
    search_fields = ['full_name', 'email', 'phone', ]
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "department":
                kwargs["queryset"] = Department.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            if db_field.name == "job_title":
                kwargs["queryset"] = JobPosition.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EmployeePrivateInfoAdmin(admin.ModelAdmin):
    list_display = ['employee', 'father_name', 'mother_name', 'gender', 'marital_status',
                    'spouse_name', 'children', 'blood_group', 'dob', 'religion', 'nationality', 'company', ]
    list_filter = [CompanylistFilter, ]
    search_fields = ['employee__full_name', ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "employee":
                kwargs["queryset"] = Employee.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'company', ]
    list_filter = [CompanylistFilter, ]
    search_fields = ['name', ]
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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


class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'company', ]
    list_filter = [CompanylistFilter, ]
    search_fields = ['name', ]
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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


class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month_year', 'basic_salary', 'conveyance', 'house_rent_allowance',
                    'medical_allowance', 'special_allowance', 'total', 'company',)
    exclude = ('total',)
    search_fields = ('employee__full_name', 'company__title',)
    list_filter = (EmployeelistFilter, CompanylistFilter,)
    list_per_page = 25
    form = PayrollModelForm

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "employee":
                kwargs["queryset"] = Employee.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date',
                    'end_date', 'reason', 'status',)
    search_fields = ('employee__full_name', 'leave_type')
    list_filter = (EmployeelistFilter, 'leave_type')
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "employee":
                kwargs["queryset"] = Employee.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status',
                    'time_in', 'time_out', 'hours',)
    search_fields = ('employee__full_name',)
    list_filter = ('status', CompanylistFilter)
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "employee":
                kwargs["queryset"] = Employee.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'city',
                    'country', 'circular', 'date', 'resume', 'company')
    search_fields = ('first_name', 'last_name',)
    list_filter = (PositionlistFilter, CompanylistFilter)
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "position":
                kwargs["queryset"] = JobPosition.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            if db_field.name == "circular":
                kwargs["queryset"] = JobCircular.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class JobCircularAdmin(admin.ModelAdmin):
    list_display = ('job_position', 'company', 'deadline', 'status',)
    search_fields = ('job_position__name', 'company__title',)
    list_filter = (PositionlistFilter, CompanylistFilter)
    list_per_page = 25

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            if request.user.is_owner and request.user.is_editor:
                return super().get_queryset(request).filter(company__owner=request.user)
            else:
                return super().get_queryset(request).filter(company=UserPreference.objects.get(user=request.user).company.id)

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

            if db_field.name == "job_position":
                kwargs["queryset"] = JobPosition.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            if db_field.name == "department":
                kwargs["queryset"] = Department.objects.filter(Q(company__owner=request.user) | Q(
                    company=UserPreference.objects.get(user=request.user).company))

            return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(JobPosition, JobPositionAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(EmployeePrivateInfo, EmployeePrivateInfoAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(JobCircular, JobCircularAdmin)
