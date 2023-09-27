from django.db.models.signals import post_save,  pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import *
from inventory.accounting.models import *

User = get_user_model()


@receiver(post_save, sender=Payroll)
def custom_user_group(sender, **kwargs):
    if kwargs['created']:
        print(kwargs['instance'])
        Transaction.objects.create(company=kwargs['instance'].company,
                                   description=kwargs['instance'].employee.full_name,
                                   account_type="Payroll",
                                   paid_amount=kwargs['instance'].total)


@receiver(post_save, sender=JobApplication)
def get_employee(sender, **kwargs):
    if kwargs['instance'].status == "APPROVED":
        Employee.objects.create(company=kwargs['instance'].company,
                                first_name=kwargs['instance'].first_name,
                                last_name=kwargs['instance'].last_name,
                                email=kwargs['instance'].email,
                                phone=kwargs['instance'].phone,
                                address=kwargs['instance'].address,
                                city=kwargs['instance'].city,
                                state=kwargs['instance'].state,
                                country=kwargs['instance'].country,
                                zip_code=kwargs['instance'].zip_code,
                                job_title=kwargs['instance'].position,
                                resume=kwargs['instance'].resume,
                                date_of_joining=kwargs['instance'].date,
                                )
