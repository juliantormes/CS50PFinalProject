# Generated by Django 5.0.3 on 2024-09-20 11:10

import django.core.validators
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0028_expenserecurringchangelog_incomerecurringchangelog'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='credit_limit',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='installments',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AddConstraint(
            model_name='expensecategory',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_category_per_user'),
        ),
        migrations.AddConstraint(
            model_name='incomecategory',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_income_category_per_user'),
        ),
    ]
