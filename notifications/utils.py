from .models import Notification

def create_notification(user, document, action):
    message = f"An admin has {action} your document '{document.name}'."
    # You can add different messages for each action if needed
    Notification.objects.create(user=user, document=document, action=action, message=message)
