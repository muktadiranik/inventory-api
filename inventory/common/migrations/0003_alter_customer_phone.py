# Generated by Django 3.2.15 on 2022-12-05 12:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator('^[0-9-+ ]+$', "Phone number must be entered in the format: '+9999-99999'. Up to 15 digits allowed.")]),
        ),
    ]
