# Generated by Django 4.1.6 on 2023-04-05 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestAccounting', '0011_alter_accountmodel_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralLedger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('debit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
    ]
