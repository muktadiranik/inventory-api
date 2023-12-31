# Generated by Django 3.2.15 on 2022-12-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_auto_20221226_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cash_in_hand',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='due',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='income_expense',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='profit_loss',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total_payable',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total_receivable',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='unit_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]
