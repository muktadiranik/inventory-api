# Generated by Django 3.2.15 on 2022-12-29 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_auto_20221228_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
