from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from hr.models import *
from inventory.common.models import *
from .serializers import *
from .models import *

# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Employee.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeePrivateInfoViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeePrivateInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeePrivateInfo.objects.filter(employee_id=self.kwargs["employee_pk"])

    def get_serializer_context(self):
        return {"employee_id": self.kwargs["employee_pk"], "request": self.request}


class JobCircularViewSet(viewsets.ModelViewSet):
    serializer_class = JobCircularSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobCircular.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class JobApplicationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return JobApplication.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = JobApplicationSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Department.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobPositionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return JobPosition.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = JobPositionSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeaveViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Leave.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Attendance.objects.filter(company__owner=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]
