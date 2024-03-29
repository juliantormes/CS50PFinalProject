# Generated by Django 5.0.2 on 2024-03-05 23:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_alter_expense_expense_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense', to='tracker.expensecategory'),
        ),
        migrations.AlterField(
            model_name='income',
            name='income_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='income', to='tracker.incomecategory'),
        ),
    ]
