# Generated by Django 5.1.3 on 2024-11-19 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0008_remove_result_grade1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='percentage',
        ),
    ]