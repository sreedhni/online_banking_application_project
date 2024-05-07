# Generated by Django 5.0.4 on 2024-04-28 23:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBranches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AccountCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Personal', 'Personal'), ('NRI', 'NRI'), ('Business', 'Business')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=100)),
                ('minimum_balance', models.PositiveIntegerField()),
                ('minimum_age', models.PositiveIntegerField()),
                ('maximum_transaction_amount_per_day', models.PositiveIntegerField()),
                ('eligibility', models.CharField(max_length=200)),
                ('account_details', models.TextField(max_length=500)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.accountcategory')),
            ],
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.accountcategory')),
            ],
        ),
    ]
