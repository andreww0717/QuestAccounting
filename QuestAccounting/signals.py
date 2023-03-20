from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserCreation





User = get_user_model()

@receiver(post_save, sender=UserCreation)
def create_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create_user(
            username=instance.username,
            email=instance.email,
            password=instance.password1,
            first_name=instance.first_name,
            last_name=instance.last_name,
            date_of_birth=instance.date_of_birth
        )

