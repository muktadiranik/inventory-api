from django.contrib import admin
from .models import *
from inventory.common.models import *


# employee admin job_title filter
class JobTitlelistFilter(admin.SimpleListFilter):
    title = "Job Title"
    parameter_name = "job_title"

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return JobPosition.objects.all().values_list("id", "name")
        else:
            if request.user.is_owner and request.user.is_editor:
                return JobPosition.objects.filter(company__owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(job_title=self.value())
        else:
            return queryset

# leave admin employee filter


class EmployeelistFilter(admin.SimpleListFilter):
    title = "Employee"
    parameter_name = "employee"

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return Employee.objects.all().values_list("id", "full_name")
        else:
            if request.user.is_owner and request.user.is_editor:
                return Employee.objects.filter(company__owner=request.user).values_list("id", "full_name")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(employee=self.value())
        else:
            return queryset


# application admin position filter
class PositionlistFilter(admin.SimpleListFilter):
    title = "Position"
    parameter_name = "position"

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return JobPosition.objects.all().values_list("id", "name")
        else:
            if request.user.is_owner and request.user.is_editor:
                return JobPosition.objects.filter(company__owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position=self.value())
        else:
            return queryset
