# Generated by Django 5.1.3 on 2024-11-18 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0002_alter_staff_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='smsapp.grade'),
        ),
    ]
