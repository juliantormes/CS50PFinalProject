# Generated by Django 5.0.2 on 2024-03-12 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0015_recurringexpensechange_recurringincomechange_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurringincomechange',
            name='income',
        ),
        migrations.CreateModel(
            name='ExpenseChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('change_date', models.DateField(auto_now_add=True)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_logs', to='tracker.expense')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('change_date', models.DateField(auto_now_add=True)),
                ('income', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_logs', to='tracker.income')),
            ],
        ),
        migrations.DeleteModel(
            name='RecurringExpenseChange',
        ),
        migrations.DeleteModel(
            name='RecurringIncomeChange',
        ),
    ]
