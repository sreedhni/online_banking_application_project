# Generated by Django 5.0.4 on 2024-04-29 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0005_account_account_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_category',
        ),
    ]
