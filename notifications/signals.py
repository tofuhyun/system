# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from folders.models import Documents  # Correct model name: Documents (plural)
# from staff.models import Users  # Correct user model import
# from notifications.models import Notification

# @receiver(post_save, sender=Documents)
# def create_notifications(sender, instance, created, **kwargs): 
#     if created:
#         # Notify the user who uploaded the document
#         Notification.objects.create(
#             recipient=instance.uploaded_by,
#             message=f"You uploaded your document '{instance.name}'."
#         )

#         # Notify all admins
#         admins = Users.objects.filter(role="admin")
#         for admin in admins:
#             Notification.objects.create(
#                 recipient=admin,
#                 message=f"{instance.uploaded_by.username} uploaded a document '{instance.name}'."
#             )

#         # Notify all employees assigned to the document (if any)
#         employees = Users.objects.filter(role="employee")
#         for employee in employees:
#             Notification.objects.create(
#                 recipient=employee,
#                 message=f"{instance.uploaded_by.username} uploaded a document '{instance.name}' assigned to you."
#             )
