# from django.urls import path
# from .views import GetDocumentFileView
# from folders import views

# urlpatterns = [
#     path('folders/', views.FolderView.as_view()),
#     path('document/', views.DocumentView.as_view()),
#     path('document/<int:id>/', views.DocumentView.as_view()),
#     path('edit-document/<int:id>/', views.DocumentView.as_view()),
#     path('delete-document/<int:id>/', views.DocumentView.as_view()),
#     path('get-document/<str:ref_num>/', views.GetDocumentRefView.as_view()),
#     path('get-document-count/', views.DocumentStatusCountView.as_view()),
#     path('api/get-document-file/<int:file_id>/', GetDocumentFileView.as_view(), name='get_document_file'),
# ]

from django.urls import path
from .views import GetDocumentFileView, FolderView, DocumentView, GetDocumentRefView, DocumentStatusCountView, AddDocumentToFolderView, RemoveDocumentFromFolderView, FolderByDepartmentView

urlpatterns = [
    path('folders/', FolderView.as_view()),
    path('document/', DocumentView.as_view()),
    path('document/<int:id>/', DocumentView.as_view()),
    path('edit-document/<int:id>/', DocumentView.as_view()),
    path('delete-document/<int:id>/', DocumentView.as_view()),
    path('get-document/<str:ref_num>/', GetDocumentRefView.as_view()),
    path('get-document-count/', DocumentStatusCountView.as_view()),
    path('api/get-document-file/<int:file_id>/', GetDocumentFileView.as_view(), name='get_document_file'),

    # New URLs for folder-document mapping
    path('document/<int:doc_id>/add-folder/<int:folder_id>/', AddDocumentToFolderView.as_view(), name='add_document_to_folder'),
    path('document/<int:doc_id>/remove-folder/<int:folder_id>/', RemoveDocumentFromFolderView.as_view(), name='remove_document_from_folder'),
    path('folders/department/<int:department_id>/', FolderByDepartmentView.as_view(), name='folders_by_department'),

]
