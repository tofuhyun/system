# from rest_framework import serializers

# from .models import Folders
# from .models import Documents

# class FolderListSerializer(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Folders
#         fields = [
#             'id',
#             'name',
#             'is_parent',
#             'is_child',
#             'parent',
#             'created_at',
#             'children'
#         ]
#     def get_children(self, obj):
#         children = Folders.objects.filter(parent=obj)
#         if children.exists():
#             return FolderListSerializer(children, many=True).data
#         return []
    
# class DocumentSerializer(serializers.ModelSerializer):
#     to_username = serializers.CharField(source='assigned_to.username', read_only=True)
#     from_username = serializers.CharField(source='from_person.username', read_only=True)
#     status_display = serializers.SerializerMethodField()
#     class Meta:
#         model =  Documents
#         fields = '__all__'
        
#     def get_status_display(self, obj):
#         return obj.get_status_display()
    

from rest_framework import serializers
from .models import Folders, Documents, FileInFolderMapping

# Folder Serializer (with department information)
class FolderListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True)  # Include department name in folder data

    class Meta:
        model = Folders
        fields = [
            'id',
            'name',
            'is_parent',
            'is_child',
            'parent',
            'created_at',
            'department_name',  # Add department_name to fields
            'children'
        ]

    def get_children(self, obj):
        children = Folders.objects.filter(parent=obj)
        if children.exists():
            return FolderListSerializer(children, many=True).data
        return []

# Document Serializer (no major changes, just including folder data as done previously)
class DocumentSerializer(serializers.ModelSerializer):
    to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    from_username = serializers.CharField(source='from_person.username', read_only=True)
    status_display = serializers.SerializerMethodField()
    folders = serializers.SerializerMethodField()  # Add folders to the document serializer
    
    class Meta:
        model = Documents
        fields = '__all__'
        
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    def get_folders(self, obj):
        # Retrieve folders that the document is part of (via the FileInFolderMapping model)
        folders = FileInFolderMapping.objects.filter(file=obj)
        if folders.exists():
            return FolderListSerializer([folder.folder for folder in folders], many=True).data
        return []

# FileInFolderMapping Serializer (no changes)
class FileInFolderMappingSerializer(serializers.ModelSerializer):
    folder_name = serializers.CharField(source='folder.name', read_only=True)
    file_title = serializers.CharField(source='file.title', read_only=True)

    class Meta:
        model = FileInFolderMapping
        fields = ['folder', 'file', 'folder_name', 'file_title', 'created_at']
        
    def create(self, validated_data):
        # Create the mapping between a file and a folder
        return FileInFolderMapping.objects.create(**validated_data)


