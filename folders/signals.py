from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Documents  

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

@receiver(post_save, sender=Documents)
def document_saved(sender, instance, created, **kwargs):
    action = 'incoming' if created else 'updated'
    notify_folder_update(instance.folder_id, action, instance.name)

@receiver(post_delete, sender=Documents)
def document_deleted(sender, instance, **kwargs):
    notify_folder_update(instance.folder_id, 'outgoing', instance.name)
