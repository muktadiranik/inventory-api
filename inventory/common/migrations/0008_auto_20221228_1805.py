# Generated by Django 3.2.15 on 2022-12-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20221215_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(choices=[('Dollar (USD)', 'Dollar (USD)'), ('Taka (BDT)', 'Taka (BDT)')], max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(choices=[('English', 'English'), ('বাংলা', 'বাংলা')], max_length=50, null=True, unique=True),
        ),
    ]
