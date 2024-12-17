# from .serializers import FolderListSerializer
# from .serializers import DocumentSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework import status
# from django.db.models import Count
# from .models import Folders,Documents
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from barcode import Code128
# from django.http import FileResponse

# from barcode.writer import ImageWriter

# import os
# from django.conf import settings

# class FolderView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self,request):
#         data = Folders.objects.filter(is_parent=True, is_child=False).order_by('id')
#         serializer = FolderListSerializer(data, many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         data = request.data
#         serializer = FolderListSerializer(data = data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class DocumentView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, id=None):
#         if id:
#             data = Documents.objects.get(id=id)
#             serializer = DocumentSerializer(data, context={'request': self.request})
#             return Response(serializer.data)
#         data = Documents.objects.order_by('id')
#         serializer = DocumentSerializer(data, many=True, context={'request': self.request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         data = request.data
#         serializer = DocumentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self,request, *args, **kwargs):
#         data = Documents.objects.get(id=kwargs['id'])
#         serializer = DocumentSerializer(data, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, *args, **kwargs):
#         try:
#             instance = Documents.objects.get(id=kwargs['id'])
#         except Documents.DoesNotExist:
#             return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

#         if not instance.status == 'disable':
#             instance.status = 'disable'
#             instance.save()
#             serializer = DocumentSerializer(instance)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         instance.delete()
#         if instance.file:
#             file_path = os.path.join(settings.MEDIA_ROOT, instance.file.name)
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#         return Response({'message': 'Document deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

# class GetDocumentRefView(APIView):
#     permission_classes = [AllowAny]
    
#     def get(self, request, **kwargs):
#         try:
#             data = Documents.objects.get(reference_number=kwargs['ref_num'])
#         except Documents.DoesNotExist:
#             return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = DocumentSerializer(data)
#         return Response(serializer.data)
    

# class GetDocumentFileView(APIView):
#     permission_classes = [AllowAny]  
    
#     def get(self, request, **kwargs):
#         try:
#             # Fetch the document by ID
#             document = Documents.objects.get(id=kwargs['file_id'])
#         except Documents.DoesNotExist:
#             return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         # Assuming the document is stored as a file in your model
#         file_path = document.file.path  # Adjust if your file storage path differs
        
#         # Return the file using FileResponse
#         return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=document.title)



    
# class DocumentStatusCountView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, **kwargs):
#         try:
#             total_documents = Documents.objects.count()

#             status_counts = Documents.objects.values('status').annotate(count=Count('status')).order_by('status')

#             status_display_map = dict(Documents.STATUS_CHOICES)

#             formatted_status_counts = [
#                 {
#                     'name': status_display_map.get(item['status'], item['status']),
#                     'count': item['count']
#                 }
#                 for item in status_counts
#             ]

#             if not formatted_status_counts:
#                 return Response({'error': 'No documents found'}, status=status.HTTP_404_NOT_FOUND)

#             return Response({
#                 'total_documents': total_documents,
#                 'status_counts': formatted_status_counts
#             }, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# class PrintDocumentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         # Fetch the document by ID
#         document = Documents.objects.get(id=id)

#         # Create a BytesIO buffer for the PDF
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer, pagesize=letter)
#         width, height = letter

#         # Barcode
#         barcode_value = str(document.id)
#         barcode = Code128(barcode_value, writer=ImageWriter())
#         barcode_filename = f"barcode_{barcode_value}.png"
#         barcode.save(barcode_filename)

#         # Draw the barcode on the PDF
#         p.drawImage(barcode_filename, 100, height - 200, width=200, height=100)

#         # PDF Content
#         p.setFont("Helvetica", 12)
#         p.drawString(100, height - 300, f"Document ID: {document.id}")
#         p.drawString(100, height - 320, f"Title: {document.title}")
#         p.drawString(100, height - 340, f"Assigned To: {document.assigned_to.username}")
#         p.drawString(100, height - 360, f"Created By: {document.from_person.username}")
#         p.drawString(100, height - 380, f"Status: {document.get_status_display()}")
#         p.drawString(100, height - 400, f"Created At: {document.created_at}")
#         p.drawString(100, height - 420, f"Updated At: {document.updated_at}")

#         # Finalize the PDF
#         p.showPage()
#         p.save()

#         # Return the PDF as a response
#         buffer.seek(0)
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="document_{document.id}.pdf"'
#         return response

from .serializers import FolderListSerializer, DocumentSerializer, FileInFolderMappingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.db.models import Count
from .models import Folders, Documents, FileInFolderMapping
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from barcode import Code128
from django.http import FileResponse
from barcode.writer import ImageWriter
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from notifications.utils import create_notification


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Folder View
class FolderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        department_id = request.query_params.get('department_id', None)
        
        if department_id:
            # Fetch folders by department if provided
            data = Folders.objects.filter(department_id=department_id).order_by('id')
        else:
            # Fetch parent folders by default
            data = Folders.objects.filter(is_parent=True, is_child=False).order_by('id')
        
        serializer = FolderListSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = FolderListSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FolderByDepartmentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, department_id):
        # Fetch folders associated with a department
        data = Folders.objects.filter(department_id=department_id).order_by('id')
        serializer = FolderListSerializer(data, many=True)
        return Response(serializer.data)
    
# Document View (no changes)
class DocumentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            data = Documents.objects.get(id=id)
            serializer = DocumentSerializer(data, context={'request': self.request})
            return Response(serializer.data)
        data = Documents.objects.order_by('id')
        serializer = DocumentSerializer(data, many=True, context={'request': self.request})
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        data = Documents.objects.get(id=kwargs['id'])
        serializer = DocumentSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = Documents.objects.get(id=kwargs['id'])
        except Documents.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not instance.status == 'disable':
            instance.status = 'disable'
            instance.save()
            serializer = DocumentSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        instance.delete()
        if instance.file:
            file_path = os.path.join(settings.MEDIA_ROOT, instance.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
        return Response({'message': 'Document deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Get Document by Reference Number
class GetDocumentRefView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, **kwargs):
        try:
            data = Documents.objects.get(reference_number=kwargs['ref_num'])
        except Documents.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DocumentSerializer(data)
        return Response(serializer.data)

# Get Document File (no changes)
class GetDocumentFileView(APIView):
    permission_classes = [AllowAny]  
    
    def get(self, request, **kwargs):
        try:
            # Fetch the document by ID
            document = Documents.objects.get(id=kwargs['file_id'])
        except Documents.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Assuming the document is stored as a file in your model
        file_path = document.file.path  # Adjust if your file storage path differs
        
        # Return the file using FileResponse
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=document.title)

# Document Status Count (no changes)
class DocumentStatusCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, **kwargs):
        try:
            total_documents = Documents.objects.count()

            status_counts = Documents.objects.values('status').annotate(count=Count('status')).order_by('status')

            status_display_map = dict(Documents.STATUS_CHOICES)

            formatted_status_counts = [
                {
                    'name': status_display_map.get(item['status'], item['status']),
                    'count': item['count']
                }
                for item in status_counts
            ]

            if not formatted_status_counts:
                return Response({'error': 'No documents found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'total_documents': total_documents,
                'status_counts': formatted_status_counts
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Print Document View (no changes)
class PrintDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Fetch the document by ID
        document = Documents.objects.get(id=id)

        # Create a BytesIO buffer for the PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Barcode
        barcode_value = str(document.id)
        barcode = Code128(barcode_value, writer=ImageWriter())
        barcode_filename = f"barcode_{barcode_value}.png"
        barcode.save(barcode_filename)

        # Draw the barcode on the PDF
        p.drawImage(barcode_filename, 100, height - 200, width=200, height=100)

        # PDF Content
        p.setFont("Helvetica", 12)
        p.drawString(100, height - 300, f"Document ID: {document.id}")
        p.drawString(100, height - 320, f"Title: {document.title}")
        p.drawString(100, height - 340, f"Assigned To: {document.assigned_to.username}")
        p.drawString(100, height - 360, f"Created By: {document.from_person.username}")
        p.drawString(100, height - 380, f"Status: {document.get_status_display()}")
        p.drawString(100, height - 400, f"Created At: {document.created_at}")
        p.drawString(100, height - 420, f"Updated At: {document.updated_at}")

        # Finalize the PDF
        p.showPage()
        p.save()

        # Return the PDF as a response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="document_{document.id}.pdf"'
        return response

# File-In-Folder View for managing folder assignments for documents
class FileInFolderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = FileInFolderMappingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, folder_id):
        # Fetch all files for a specific folder
        data = FileInFolderMapping.objects.filter(folder_id=folder_id)
        serializer = FileInFolderMappingSerializer(data, many=True)
        return Response(serializer.data)
    
    def delete(self, request, folder_id, file_id):
        try:
            mapping = FileInFolderMapping.objects.get(folder_id=folder_id, file_id=file_id)
            mapping.delete()
            return Response({'message': 'File removed from folder'}, status=status.HTTP_204_NO_CONTENT)
        except FileInFolderMapping.DoesNotExist:
            return Response({'error': 'File not found in folder'}, status=status.HTTP_404_NOT_FOUND)




class AddDocumentToFolderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, doc_id, folder_id):
        # Fetch the document and folder instances
        document = get_object_or_404(Documents, id=doc_id)
        folder = get_object_or_404(Folders, id=folder_id)
        
        # Check if the folder is a parent folder
        if not folder.is_parent:
            return Response({'error': 'You can only add documents to parent folders.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the association between the document and folder
        mapping, created = FileInFolderMapping.objects.get_or_create(document=document, folder=folder)
        
        if created:
            return Response({'message': 'Document added to folder successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Document is already in this folder.'}, status=status.HTTP_200_OK)



class RemoveDocumentFromFolderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, doc_id, folder_id):
        # Fetch the document and folder instances
        document = get_object_or_404(Documents, id=doc_id)
        folder = get_object_or_404(Folders, id=folder_id)
        
        # Check if the folder is a parent folder
        if not folder.is_parent:
            return Response({'error': 'You can only remove documents from parent folders.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Try to find and delete the mapping
            mapping = FileInFolderMapping.objects.get(document=document, folder=folder)
            mapping.delete()
            return Response({'message': 'Document removed from folder successfully.'}, status=status.HTTP_200_OK)
        except FileInFolderMapping.DoesNotExist:
            return Response({'error': 'No such document-folder association exists.'}, status=status.HTTP_404_NOT_FOUND)


def update_document_status(request, doc_id, new_status):
    document = Documents.objects.get(id=doc_id)
    # Assuming 'user' is the user who uploaded the document
    user = document.user  # Or however the document is associated with a user
    
    # Update the document's status
    document.status = new_status
    document.save()

    # Create a notification for the user
    create_notification(user, document, new_status)
    
    # Create notification for the employee (or admin, if needed)
    # You can send notifications to the admin or employee as needed.
    
    return Response({'status': 'success'}, status=200)


def notify_folder_update(folder_id, action, file_name):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'folder_updates',
        {
            'type': 'folder_message',
            'message': {
                'folder_id': folder_id,
                'action': action,
                'file_name': file_name,
            }
        }
    )

# Example usage inside a view
class FileMoveView(APIView):
    def post(self, request):
        folder_id = request.data['folder_id']
        action = request.data['action']  # 'incoming' or 'outgoing'
        file_name = request.data['file_name']

        # Trigger WebSocket notification
        notify_folder_update(folder_id, action, file_name)

        return Response({"message": "File update notification sent"})

