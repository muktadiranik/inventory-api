# Generated by Django 3.2.15 on 2023-01-06 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='discount',
            field=models.IntegerField(blank=True, help_text='Discount in percentage', null=True),
        ),
    ]
