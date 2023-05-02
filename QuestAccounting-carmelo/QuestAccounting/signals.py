from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import  AccountModel, EventLog





User = get_user_model()

# how event logs are saved when an account is created or edited


account_changed = Signal()

@receiver(account_changed)
def log_account_model_change_pre_save(sender, user, instance, new, **kwargs):
    print(new)
    if instance.pk:
        # checks if account is new or not and sets the before_image accordingly
        if new:
            
            before_image = None
        else:
            
            before_image = AccountModel.objects.get(pk=instance.pk)
        after_image = instance
        account_name = instance.account_name
        
        before_change = {}
        after_change = {}

        # find the fields that have changed and combine them into before_change and after_change
        for field in instance._meta.fields:
            if new:
                before_value = None
            else:
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

        # if there is no data for before_change (new account) then create eventlog with empty before_image
        if not before_change and after_change:
            EventLog.objects.create(
                account_changed=account_name,
                before_image=None,
                after_image=after_change,
                user=user
            )
            return
        
        # if account is not new create eventlog with before and after info else its new so before will be empty
        if not new:
            EventLog.objects.create(
                account_changed=account_name,
                before_image=before_change,
                after_image=after_change,
                user=user
            )
        else: 
            EventLog.objects.create(
                account_changed=account_name,
                before_image=None,
                after_image=after_change,
                user=user
            )

        

