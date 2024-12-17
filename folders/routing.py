from django.urls import path
from folders.consumers import FolderUpdateConsumer

websocket_urlpatterns = [
    path('ws/folders/', FolderUpdateConsumer.as_asgi()),
]
