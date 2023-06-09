from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from django.contrib.auth.models import User, Group
from QuestAccounting import models
from django.core.mail import send_mail
from .models import AccountRequest, UserProfile, AccountModel, JournalEntriesModel




userList = User.objects.values_list('username', flat = True)

# form that holds info for creating a user request
class UserCreationRequest(models.ModelForm):
    class Meta:
        model = AccountRequest
        fields = ['first_name', 'last_name', 'date_of_birth', 'email']

    def save(self, *args, **kwargs):
        # Sends email notification when a new request is submitted
        if self.instance.pk is None:
            send_mail(
                'New user creation request',
              f'A new user creation request has been submitted:\n\nEmail: {self.instance.email}\nFirst name: {self.instance.first_name}\nLast name: {self.instance.last_name}\n\nDate of birth: {self.instance.date_of_birth}\nIf this user is approved, please create the user account and send them the login info with a temporary password.',

                'noreply@QuestAccounting.com',
                ['AppDomainQuestA@gmail.com'],
                fail_silently=False,
            )
        return super().save(*args, **kwargs)
    
# form that holds info for created user
class UserCreation(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    date_of_birth = forms.DateField(required=True)
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','date_of_birth', 'email', 'password1', 'password2']

    def save(self, *args, **kwargs):
        # Sends email notification to user when account is created
        if self.instance.pk is None:
            password = self.cleaned_data.get('password1')
            send_mail(
                'Account Request Approved',
              f'Here are your login credentials:\n\nEmail: {self.instance.email}\nFirst name: {self.instance.first_name}\nLast name: {self.instance.last_name}\nUsername: {self.instance.username}\nPassword: {password}\n\nLogin and change your password as soon as you can and welcome to Quest Accounting!',

                'noreply@QuestAccounting.com',
                [self.instance.email],
                fail_silently=False,
            )
        return super().save(*args, **kwargs)
    
# form for editting a users information
class EditUser(forms.ModelForm):
    username = forms.CharField(max_length=30, required = True)
    first_name = forms.CharField(max_length=30, required = True)
    last_name = forms.CharField(max_length=30, required = True)
    email = forms.EmailField(required = True)
    is_active = forms.BooleanField(required = False)
    previous_page = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

# form that takes the user's email for password reset
class PasswordReset(PasswordResetForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ['email']

# form that adds profile pic for user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control-file'})

# form that holds info for accounts being created in chart of accounts
class AccountForm(forms.ModelForm):
    class Meta:
        model = AccountModel
        fields = ['account_name', 'account_number','account_description','normal_side','account_category','account_subcategory','initial_balance','debit','credit','balance','user_id','order','statement','comment', 'activated']

# form to select user group
class GroupSelection(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    
    class Meta:
        model = Group
        fields = ['group']

#form that holds journal entry info
class JournalEntriesForm(forms.ModelForm):
    class Meta:
        model = JournalEntriesModel
        fields = ['account_name', 'debit', 'credit']

# form that holds email info to send to users
class EmailForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)