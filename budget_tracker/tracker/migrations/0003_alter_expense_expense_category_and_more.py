# Generated by Django 5.0.2 on 2024-03-05 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_incomecategory_rename_category_expensescategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expenses', to='tracker.expensescategory'),
        ),
        migrations.AlterField(
            model_name='income',
            name='income_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='income', to='tracker.incomecategory'),
        ),
    ]
