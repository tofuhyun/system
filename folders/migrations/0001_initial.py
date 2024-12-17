# Generated by Django 5.1 on 2024-10-06 02:44

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['docx', 'pdf', 'xlsx', 'csv', 'txt', 'jpg', 'png', 'img'])])),
                ('file_type', models.CharField(blank=True, max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('archived', 'Archived'), ('disable', 'Disable'), ('pending', 'Pending')], default='pending', max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('reference_number', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('document_type', models.CharField(blank=True, choices=[('AIP', 'AIP'), ('Advisory', 'Advisory'), ('Application Letter', 'Application Letter'), ('Authority to Travel', 'Authority to Travel'), ('COC-DPWH', 'COC-DPWH'), ('Certificate of No Pending Case', 'Certificate of No Pending Case'), ('Class Observation Plan', 'Class Observation Plan'), ('Communications', 'Communications'), ('Conduct Research', 'Conduct Research'), ('Daily Time Record (DTR)', 'Daily Time Record (DTR)'), ('Designation Letter', 'Designation Letter'), ('Disbursement Voucher', 'Disbursement Voucher'), ('Division Clearance', 'Division Clearance'), ('ERF', 'ERF'), ('Endorsement of Transfer to other Division', 'Endorsement of Transfer to other Division'), ('Fidelity Bond', 'Fidelity Bond'), ('GSIS Maturity & Retirement Form', 'GSIS Maturity & Retirement Form'), ('Instructional Supervisory Plan', 'Instructional Supervisory Plan'), ('Itinerary of Travel', 'Itinerary of Travel'), ('Job Order', 'Job Order'), ('Leave Application', 'Leave Application'), ('Legal Documents', 'Legal Documents')], max_length=50, null=True)),
                ('other_document_type', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
                ('from_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_parent', models.BooleanField(default=False)),
                ('is_child', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='folders.folders')),
            ],
        ),
    ]
