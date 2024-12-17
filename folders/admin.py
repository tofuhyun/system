from django.contrib import admin
from .models import Folders, Documents, FileInFolderMapping, Department

# Registering the Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']
    ordering = ['name']

# Registering the Folders model
@admin.register(Folders)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_parent', 'is_child', 'parent', 'department', 'created_at']
    search_fields = ['name', 'id']
    list_filter = ['is_parent', 'is_child', 'parent', 'department']
    ordering = ['created_at']

# Registering the Documents model
@admin.register(Documents)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file', 'file_type', 'uploaded_at', 'status', 'assigned_to', 'from_person', 'reference_number', 'document_type', 'other_document_type', 'updated_at']
    search_fields = ['title', 'reference_number', 'status', 'assigned_to__username', 'from_person__username']
    list_filter = ['status', 'document_type', 'assigned_to', 'from_person']
    ordering = ['uploaded_at']

# Registering the FileInFolderMapping model
@admin.register(FileInFolderMapping)
class FileInFolderMappingAdmin(admin.ModelAdmin):
    list_display = ['folder', 'file', 'created_at']
    search_fields = ['folder__name', 'file__title']
    list_filter = ['folder', 'created_at']
    ordering = ['created_at']
