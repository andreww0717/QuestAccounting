# Generated by Django 4.1.6 on 2023-04-03 21:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestAccounting', '0010_alter_accountmodel_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmodel',
            name='account_number',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$', 'Enter a valid number.')]),
        ),
    ]
