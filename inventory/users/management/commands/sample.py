from django.core.management.base import BaseCommand
from inventory.accounting.models import Transaction
from inventory.subscription.models import Plan, Subscriber
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create sample data for testing"

    def create_superuser(self, first_name, last_name, email, password):
        users = User.objects.filter(email=email)
        num = len(users)
        if num:
            print('User: ' + email + ' password: ' + password + ' already exists')
            return

        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_superuser=True,
            is_active=True,
            is_staff=True,

        )
        print('User: ' + email + ' password: ' + password)

    def handle(self, *args, **kwargs):
        self.create_superuser(
            first_name='Shohel',
            last_name='Rana',
            password='sohel-22',
            email='shohel@devxhub.com',
        )
        self.create_superuser(
            first_name='Hadisur ',
            last_name='Rahman',
            password='hadisur-22',
            email='hadis@devxhub.com',
        )
        self.create_superuser(
            first_name='Eliyas',
            last_name='Hossain',
            password='elias-74',
            email='eliyas@devxhub.com',
        )
        self.create_superuser(
            first_name='Anik',
            last_name='Muktadir',
            password='admin',
            email='admin@gmail.com',
        )

        print('Superuser created successfully')


# python manage.py sample
