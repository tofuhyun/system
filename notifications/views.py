# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from rest_framework.permissions import IsAuthenticated

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        data = [{'message': notif.message, 'created_at': notif.created_at} for notif in notifications]
        return Response(data)
