from django import forms
from .models import *


class TransactionModelForm(forms.ModelForm):
    ACCOUNT_TYPES = [
        ('Expense', 'Expense'),
        ('Income', 'Income',),
        ('Due Pay', 'Due Pay'),
        ('Due Receive', 'Due Receive'),
        ('Invest', 'Invest'),
    ]
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
            'buyer_seller': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ProductModelForm(forms.ModelForm):
    UNIT_CHOICES = [
        ('Piece', 'Piece'),
        ('Kg', 'Kg'),
        ('Gram', 'Gram'),
        ('Litre', 'Litre'),
        ('Box', 'Box'),
        ('Pound', 'Pound'),
        ('Dozen', 'Dozen'),
        ('Other', 'Other'),
    ]
    unit = forms.ChoiceField(choices=UNIT_CHOICES)

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
