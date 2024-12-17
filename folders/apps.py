# from django.apps import AppConfig


# class FoldersConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'folders'

from django.apps import AppConfig



class FoldersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'folders'

    def ready(self):
        import folders.signals  # Ensure signals are registered when the app is ready



