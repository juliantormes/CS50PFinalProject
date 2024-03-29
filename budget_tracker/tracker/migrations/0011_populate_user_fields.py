# Generated by Django 5.0.2 on 2024-03-10 13:46

from django.db import migrations

def assign_user_to_models(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    ExpenseCategory = apps.get_model('your_app_name', 'ExpenseCategory')
    Expense = apps.get_model('your_app_name', 'Expense')
    IncomeCategory = apps.get_model('your_app_name', 'IncomeCategory')
    Income = apps.get_model('your_app_name', 'Income')

    default_user = User.objects.filter(is_superuser=True).first()
    if not default_user:
        default_user = User.objects.first()

    if default_user:
        ExpenseCategory.objects.filter(user__isnull=True).update(user=default_user)
        IncomeCategory.objects.filter(user__isnull=True).update(user=default_user)

        for expense in Expense.objects.filter(user__isnull=True):
            expense.user = default_user
            expense.save()

        for income in Income.objects.filter(user__isnull=True):
            income.user = default_user
            income.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_expense_user_expensecategory_user_income_user_and_more'),
    ]

    operations = [
    ]
