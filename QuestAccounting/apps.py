from django.apps import AppConfig
from django.db.models.signals import post_save



class QuestaccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QuestAccounting'
    def ready(self):
        # Import the User model
        from django.contrib.auth.models import User
        
        # Import the create_user function
        from .signals import create_user
        from QuestAccounting.models import UserCreation

        # Register the signal handler
        post_save.connect(create_user, sender=UserCreation, dispatch_uid='create_user')