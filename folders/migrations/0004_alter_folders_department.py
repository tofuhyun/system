# Generated by Django 5.1 on 2024-11-26 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0003_department_folders_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folders',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='folders.department'),
        ),
    ]
