# Generated by Django 3.2.15 on 2023-01-03 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_alter_faq_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'FAQ', 'verbose_name_plural': 'Faqs'},
        ),
    ]
