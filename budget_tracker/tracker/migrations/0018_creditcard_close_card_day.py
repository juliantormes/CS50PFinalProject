# Generated by Django 5.0.2 on 2024-03-13 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0017_expense_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='close_card_day',
            field=models.IntegerField(default=21),
        ),
    ]
