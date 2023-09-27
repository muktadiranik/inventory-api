from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import *

User = get_user_model()

global stock


@receiver(pre_save, sender=Transaction)
def get_product_stock_pre_save(sender, **kwargs):
    global stock
    stock = 0
    try:
        stock = Transaction.objects.get(id=kwargs["instance"].id).quantity
    except:
        stock = 0


@receiver(post_save, sender=Transaction)
def update_product_on_transaction_save_or_update(sender, **kwargs):
    global stock
    if kwargs['created']:
        if kwargs["instance"].account_type == "Expense":
            product = Product.objects.get(id=kwargs["instance"].product.id)
            product.stock += kwargs["instance"].quantity
            product.save()
        elif kwargs["instance"].account_type == "Income":
            product = Product.objects.get(id=kwargs["instance"].product.id)
            product.stock -= kwargs["instance"].quantity
            product.save()
    if not kwargs['created']:
        if kwargs["instance"].account_type == "Expense":
            product = Product.objects.get(id=kwargs["instance"].product.id)
            product.stock -= stock
            product.stock += kwargs["instance"].quantity
            product.save()
        elif kwargs["instance"].account_type == "Income":
            product = Product.objects.get(id=kwargs["instance"].product.id)
            product.stock += stock
            product.stock -= kwargs["instance"].quantity
            product.save()


@receiver(post_delete, sender=Transaction)
def update_product_on_transaction_delete(sender, **kwargs):
    if kwargs["instance"].account_type == "Expense":
        product = Product.objects.get(id=kwargs["instance"].product.id)
        product.stock -= kwargs["instance"].quantity
        product.save()
    elif kwargs["instance"].account_type == "Income":
        product = Product.objects.get(id=kwargs["instance"].product.id)
        product.stock += kwargs["instance"].quantity
        product.save()
