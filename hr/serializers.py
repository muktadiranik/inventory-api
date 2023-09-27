from rest_framework.serializers import ModelSerializer
from hr.models import *
from inventory.common.models import *


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'country',
            'zip_code',
            'department',
            'job_title',
            'salary',
            'resume',
            'date_of_joining',
        )

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class EmployeePrivateInfoSerializer(ModelSerializer):
    class Meta:
        model = EmployeePrivateInfo
        fields = '__all__'


class JobApplicationSerializer(ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        exclude = ["company"]

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class JobCircularSerializer(ModelSerializer):
    class Meta:
        model = JobCircular
        fields = '__all__'


class JobCircularSerializer(ModelSerializer):
    class Meta:
        model = JobCircular
        exclude = ["company"]

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class JobPositionSerializer(ModelSerializer):
    class Meta:
        model = JobPosition
        exclude = ["company"]

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class LeaveSerializer(ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def create(self, validated_data):
        company = UserPreference.objects.get(user=self.context["request"].user).company
        validated_data["company"] = company
        return super().create(validated_data)


class PayrollSerializer(ModelSerializer):

    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ["total"]
