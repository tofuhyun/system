# from django.db import models
# from staff.models import Users
# from django.core.validators import FileExtensionValidator
# import os
# import uuid
# from django.utils import timezone
# # Create your models here.
# class Folders(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     is_parent = models.BooleanField(default=False)
#     is_child= models.BooleanField(default=False)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null = True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
# class Documents(models.Model):
#     STATUS_CHOICES = [
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('archived', 'Archived'),
#         ('disable', 'Disable'),
#         ('pending', 'Pending')
#     ]
    
#     DOCUMENT_TYPE_CHOICES = [
#         ('AIP', 'AIP'),
#         ('Advisory', 'Advisory'),
#         ('Application Letter', 'Application Letter'),
#         ('Authority to Travel', 'Authority to Travel'),
#         ('COC-DPWH', 'COC-DPWH'),
#         ('Certificate of No Pending Case', 'Certificate of No Pending Case'),
#         ('Class Observation Plan', 'Class Observation Plan'),
#         ('Communications', 'Communications'),
#         ('Conduct Research', 'Conduct Research'),
#         ('Daily Time Record (DTR)', 'Daily Time Record (DTR)'),
#         ('Designation Letter', 'Designation Letter'),
#         ('Disbursement Voucher', 'Disbursement Voucher'),
#         ('Division Clearance', 'Division Clearance'),
#         ('ERF', 'ERF'),
#         ('Endorsement of Transfer to other Division', 'Endorsement of Transfer to other Division'),
#         ('Fidelity Bond', 'Fidelity Bond'),
#         ('GSIS Maturity & Retirement Form', 'GSIS Maturity & Retirement Form'),
#         ('Instructional Supervisory Plan', 'Instructional Supervisory Plan'),
#         ('Itinerary of Travel', 'Itinerary of Travel'),
#         ('Job Order', 'Job Order'),
#         ('Leave Application', 'Leave Application'),
#         ('Legal Documents', 'Legal Documents'),
#     ]
    
#     title = models.CharField(max_length=100)
#     file = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(allowed_extensions=['docx','pdf','xlsx','csv','txt','jpg','png','img'])])
#     file_type = models.CharField(max_length=10, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     assigned_to = models.ForeignKey(Users, on_delete=models.CASCADE, blank = True, null = True, related_name="to_user")
#     from_person = models.ForeignKey(Users, on_delete=models.CASCADE, null = False, blank = False, related_name="from_user")
#     remarks = models.TextField(blank=True, null=True)
#     reference_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
#     document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True)
#     other_document_type = models.CharField(max_length=100, blank=True, null=True)
#     updated_at = models.DateTimeField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.file:
#             _, file_extension = os.path.splitext(self.file.name)
#             self.file_type = file_extension.upper().strip('.')
#         if self.document_type:
#             self.other_document_type = None
#         if not self.reference_number:
#             self.reference_number = self.generate_reference_number()
#         self.updated_at = timezone.now()
#         super(Documents, self).save(*args, **kwargs)
        
#     def generate_reference_number(self):
#         date_str = timezone.now().strftime('%Y%m%d')
#         uid = uuid.uuid4().hex[:6].upper()
#         file_type_str = self.file_type if self.file_type else "UNK"
#         return f"DOC-{date_str}-{file_type_str}-{uid}"


from django.db import models
from staff.models import Users
from django.core.validators import FileExtensionValidator
import os
import uuid
from django.utils import timezone

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Folder Model
class Folders(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    # Retrieve all files in the folder
    def get_files(self):
        return Documents.objects.filter(fileinfoldermapping__folder=self)

    # Retrieve all subfolders
    def get_subfolders(self):
        return Folders.objects.filter(parent=self)

# Documents Model
class Documents(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('disable', 'Disable'),
        ('pending', 'Pending')
    ]
    
    DOCUMENT_TYPE_CHOICES = [
        # Add document types here
    ]
    
    title = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='documents/', 
        validators=[FileExtensionValidator(allowed_extensions=['docx', 'pdf', 'xlsx', 'csv', 'txt', 'jpg', 'png', 'img'])]
    )
    file_type = models.CharField(max_length=10, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="to_user")
    from_person = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False, related_name="from_user")
    remarks = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True)
    other_document_type = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            _, file_extension = os.path.splitext(self.file.name)
            self.file_type = file_extension.upper().strip('.')
        if self.document_type:
            self.other_document_type = None
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        self.updated_at = timezone.now()
        super(Documents, self).save(*args, **kwargs)
        
    def generate_reference_number(self):
        date_str = timezone.now().strftime('%Y%m%d')
        uid = uuid.uuid4().hex[:6].upper()
        file_type_str = self.file_type if self.file_type else "UNK"
        return f"DOC-{date_str}-{file_type_str}-{uid}"

# Model to Relate Folders and Files
class FileInFolderMapping(models.Model):
    folder = models.ForeignKey(Folders, on_delete=models.CASCADE, related_name='file_mappings')
    file = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='folder_mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('folder', 'file')  # Prevent duplicates.

    def __str__(self):
        return f"{self.file.title} in {self.folder.name}"

