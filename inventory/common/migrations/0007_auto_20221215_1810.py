# Generated by Django 3.2.15 on 2022-12-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20221213_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='total_due',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='total_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
