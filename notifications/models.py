from django.db import models
from staff.models import Users
from folders.models import Documents

class Notification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        # Assuming 'title' exists in the Documents model
        return f"Notification for {self.user.username} about {self.document.title} - {self.action}"
