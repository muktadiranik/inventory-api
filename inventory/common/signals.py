from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import *
from inventory.accounting.models import *

User = get_user_model()


@receiver(post_save, sender=Company)
def create_company_user_on_company_create(sender, **kwargs):
    if kwargs['created']:
        if not CompanyUser.objects.filter(user__email=kwargs['instance'].owner.email).first():
            CompanyUser.objects.create(company=kwargs["instance"],
                                       user=User.objects.get(email=kwargs['instance'].owner))


@receiver(post_save, sender=CompanyUser)
def create_user_preference_on_company_user_create(sender, **kwargs):
    if kwargs['created']:
        try:
            user_preference = get_object_or_404(UserPreference, user__email=kwargs['instance'].company.owner.email)
            if user_preference:
                UserPreference.objects.update_or_create(
                    user=kwargs["instance"].user,
                    company=kwargs["instance"].company,
                    currency=user_preference.currency,
                    language=user_preference.language,
                )
        except:
            pass


@receiver(post_save, sender=Transaction)
def update_customer_on_transaction_save(sender, **kwargs):
    global customer
    try:
        customer = Customer.objects.get(id=kwargs["instance"].buyer_seller.id)
    except:
        return
    if customer:
        paid_amount = Transaction.objects.filter(buyer_seller=kwargs["instance"].buyer_seller).aggregate(
            Sum('paid_amount'))["paid_amount__sum"]
        income_expense = Transaction.objects.filter(buyer_seller=kwargs["instance"].buyer_seller).aggregate(
            Sum('income_expense'))["income_expense__sum"]
        customer.total_paid = paid_amount
        if kwargs["instance"].account_type == "Invest":
            customer.total_due = 0
        else:
            customer.total_due = income_expense - paid_amount
        """
        if kwargs["instance"].account_type == "Due Pay" or kwargs["instance"].account_type == "Due Receive":
            customer.total_due -= paid_amount
        """
        customer.save()


@receiver(post_delete, sender=Transaction)
def update_customer_on_transaction_delete(sender, **kwargs):
    global customer
    try:
        customer = Customer.objects.get(id=kwargs["instance"].buyer_seller.id)
    except:
        return

    if customer:
        paid_amount = Transaction.objects.filter(buyer_seller=kwargs["instance"].buyer_seller).aggregate(
            Sum('paid_amount'))["paid_amount__sum"]

        due = Transaction.objects.filter(buyer_seller=kwargs["instance"].buyer_seller).aggregate(
            Sum('due'))["due__sum"]
        if paid_amount is None:
            paid_amount = 0
        if due is None:
            due = 0
        customer.total_paid = paid_amount
        customer.total_due = due
        """
        if kwargs["instance"].account_type == "Due Pay" or kwargs["instance"].account_type == "Due Receive":
            customer.total_due -= paid_amount
        """
        customer.save()
