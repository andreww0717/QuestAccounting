from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserCreation, AccountModel, EventLog





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




User = get_user_model()

account_changed = Signal()

@receiver(account_changed)
def log_account_model_change_pre_save(sender, user, instance, new, **kwargs):
    print(new)
    if instance.pk:
        if new:
            print('1')
            before_image = None
        else:
            print('2')
            before_image = AccountModel.objects.get(pk=instance.pk)
        after_image = instance
        account_name = instance.account_name
        
        before_change = {}
        after_change = {}

        for field in instance._meta.fields:
            if new:
                print('3')
                before_value = None
            else:
                print('4')
                before_value = getattr(before_image, field.name)
            
            after_value = getattr(after_image, field.name)
            if before_value != after_value:
                before_change[field.verbose_name] = before_value
                after_change[field.verbose_name] = after_value
                
        # Check if there were any changes
        if not before_change and not after_change:
            return
            
        # create readable output for before_image
        if not new:
            print('5')
            before_image_output = ''
            for key, value in before_image.__dict__.items():
                if key.startswith('_'):
                    continue
                if key in before_change:
                    before_image_output += f'{key}: {before_change[key]}\n'
                else:
                    before_image_output += f'{key}: {value}\n'
            
        # create readable output for after_image
        after_image_output = ''
        for key, value in after_image.__dict__.items():
            if key.startswith('_'):
                continue
            if key in after_change:
                after_image_output += f'{key}: {after_change[key]}\n'
            else:
                after_image_output += f'{key}: {value}\n'

        if not before_change and after_change:
            EventLog.objects.create(
                account_changed=account_name,
                before_image=None,
                after_image=after_change,
                user=user
            )
            return
        
        if not new:
            print('6')
            EventLog.objects.create(
                account_changed=account_name,
                before_image=before_change,
                after_image=after_change,
                user=user
            )
        else: 
            print('7')
            EventLog.objects.create(
                account_changed=account_name,
                before_image=None,
                after_image=after_change,
                user=user
            )

        

