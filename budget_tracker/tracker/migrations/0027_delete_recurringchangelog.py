# Generated by Django 5.0.3 on 2024-08-27 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0026_remove_incomechangelog_income_recurringchangelog_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecurringChangeLog',
        ),
    ]
