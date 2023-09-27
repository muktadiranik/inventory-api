from django.db import models
from inventory.common.models import Company, Customer
from inventory.common.validators import *
from django.db.models.aggregates import Sum
from auditlog.registry import auditlog


ACCOUNT_TYPES = [
    ('Expense', 'Expense'),
    ('Income', 'Income',),
    ('Due Pay', 'Due Pay'),
    ('Due Receive', 'Due Receive'),
    ('Invest', 'Invest'),
    ('Payroll', 'Payroll'),
]


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


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


auditlog.register(ProductCategory)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True, help_text="Unit of the product")
    stock = models.IntegerField(blank=True, null=True, default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


auditlog.register(Product)


class Transaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    buyer_seller = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True, default=0, validators=[quantity_validator])
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True,
                                     null=True, default=0, validators=[unit_price_validator])
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES, null=True)
    income_expense = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                      default=0, validators=[paid_amount_validator])
    due = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    total_balance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    cash_in_hand = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    total_receivable = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    total_payable = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    profit_loss = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return str(self.buyer_seller)

    def save(self, *args, **kwargs):
        if self.account_type == 'Due Pay' or self.account_type == 'Due Receive' or self.account_type == 'Invest' or self.account_type == 'Payroll':
            income_expense = 0
            due = 0
        else:
            income_expense = self.quantity * self.unit_price
            due = income_expense - self.paid_amount
        try:
            if self.id is None:
                last_row = Transaction.objects.filter(company_id=self.company_id).order_by("id").reverse()[0]
            else:
                last_row = Transaction.objects.filter(company_id=self.company_id).order_by("id").reverse()[1]
        except:
            last_row = None

        if last_row:
            if self.account_type == "Expense":
                self.total_balance = last_row.total_balance - income_expense
                self.cash_in_hand = last_row.cash_in_hand - self.paid_amount
                self.total_receivable = last_row.total_receivable
                self.total_payable = last_row.total_payable + due
                self.profit_loss = last_row.profit_loss - income_expense

            if self.account_type == "Payroll":
                self.total_balance = last_row.total_balance - self.paid_amount
                self.cash_in_hand = last_row.cash_in_hand - self.paid_amount
                self.total_receivable = last_row.total_receivable
                self.total_payable = last_row.total_payable + due
                self.profit_loss = last_row.profit_loss - income_expense

            if self.account_type == "Income":
                self.total_balance = last_row.total_balance + income_expense
                self.cash_in_hand = last_row.cash_in_hand + self.paid_amount
                self.total_receivable = last_row.total_receivable + due
                self.total_payable = last_row.total_payable
                self.profit_loss = last_row.profit_loss + income_expense

            if self.account_type == "Due Pay":
                self.total_balance = last_row.total_balance
                self.cash_in_hand = last_row.cash_in_hand - self.paid_amount
                self.total_receivable = last_row.total_receivable
                self.total_payable = last_row.total_payable - self.paid_amount
                self.profit_loss = last_row.profit_loss - income_expense

            if self.account_type == "Due Receive":
                self.total_balance = last_row.total_balance
                self.cash_in_hand = last_row.cash_in_hand + self.paid_amount
                self.total_payable = last_row.total_payable
                self.total_receivable = last_row.total_receivable - self.paid_amount
                self.profit_loss = last_row.profit_loss - income_expense

            if self.account_type == "Invest":
                self.total_balance = last_row.total_balance + self.paid_amount
                self.cash_in_hand = last_row.cash_in_hand + self.paid_amount
                self.total_payable = last_row.total_payable
                self.total_receivable = last_row.total_receivable
                self.profit_loss = last_row.profit_loss + self.paid_amount

            # if last_row.cash_in_hand <= self.paid_amount and self.account_type == "Expense":
            #     pass
            # else:
            #     self.income_expense = income_expense
            #     self.due = due

            self.income_expense = income_expense
            self.due = due

        else:
            if self.account_type == "Expense":
                self.total_balance = 0 - income_expense
                self.cash_in_hand = 0 - self.paid_amount
                self.total_receivable = 0
                self.total_payable = 0 + due
                self.profit_loss = 0 - income_expense

            if self.account_type == "Payroll":
                self.total_balance = 0 - self.paid_amount
                self.cash_in_hand = 0 - self.paid_amount
                self.total_receivable = 0
                self.total_payable = 0 + due
                self.profit_loss = 0 - income_expense

            if self.account_type == "Income":
                self.total_balance = 0 + income_expense
                self.cash_in_hand = 0 + self.paid_amount
                self.total_receivable = 0 + due
                self.total_payable = 0
                self.profit_loss = 0 + income_expense

            if self.account_type == "Due Pay":
                self.total_balance = 0
                self.cash_in_hand = 0 - self.paid_amount
                self.total_receivable = 0
                self.total_payable = 0 - self.paid_amount
                self.profit_loss = 0 - income_expense

            if self.account_type == "Due Receive":
                self.total_balance = 0
                self.cash_in_hand = 0 + self.paid_amount
                self.total_payable = 0
                self.total_receivable = 0 - self.paid_amount
                self.profit_loss = 0 - income_expense

            if self.account_type == "Invest":
                self.total_balance = 0 + self.paid_amount
                self.cash_in_hand = 0 + self.paid_amount
                self.total_payable = 0
                self.total_receivable = 0
                self.profit_loss = self.paid_amount

            self.income_expense = income_expense
            self.due = due

        """
        total_Invest = Transaction.objects.filter(company_id=self.company_id, account_type="Invest").aggregate(Sum('Invest'))['Invest__sum']
        """

        total_expense = Transaction.objects.filter(company=self.company, account_type='Expense').aggregate(
            Sum('income_expense'))['income_expense__sum']

        total_Income = Transaction.objects.filter(company=self.company, account_type='Income').aggregate(
            Sum('income_expense'))['income_expense__sum']

        """
        self.total_Income = total_Income
        profit_loss = total_Income - total_expense
        self.profit_loss = profit_loss
        """

        """
        self.profit_loss = self.cash_in_hand + self.total_receivable - self.total_payable - total_Investment
        """

        total_investment = Transaction.objects.filter(
            company=self.company, account_type='Invest').aggregate(Sum('paid_amount'))['paid_amount__sum']

        # if total_investment is None:
        #     total_investment = 0

        # if self.account_type == "Invest":
        #     self.profit_loss = self.paid_amount + total_investment
        # else:
        #     self.profit_loss = self.total_balance - total_investment

        super(Transaction, self).save(*args, **kwargs)


auditlog.register(Transaction)


class ChartOfAccount(models.Model):
    name = models.CharField(max_length=255, null=True)
    value = models.DecimalField(max_digits=20, decimal_places=2,  null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.value = self.parent.value
        super(ChartOfAccount, self).save(*args, **kwargs)


auditlog.register(ChartOfAccount)
