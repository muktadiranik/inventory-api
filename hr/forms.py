from django import forms
from django_yearmonth_widget.widgets import DjangoYearMonthWidget
from django.utils.translation import gettext_lazy as _
from .models import *


class PayrollModelForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'
        widgets = {
            "company": forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'month_year': DjangoYearMonthWidget(attrs={'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'conveyance': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_rent_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = ()
        help_texts = {
            'in_time': _("Enter time of entry"),
            'out_time': _("Enter time of exit"),
        }
