# Generated by Django 4.1.6 on 2023-03-22 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuestAccounting', '0003_rename_temp_password_usercreation_password1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercreation',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='usercreation',
            name='created_at',
        ),
    ]