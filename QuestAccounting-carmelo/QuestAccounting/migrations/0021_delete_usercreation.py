# Generated by Django 4.1.6 on 2023-04-12 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuestAccounting', '0020_remove_eventlog_event_type_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCreation',
        ),
    ]
