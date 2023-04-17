from django.db import models, migrations
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.forms import ModelChoiceField, ModelForm
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator

# adds the database that tracks user requests
class AccountRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField()

# adds the database that tracks users and their profile pictures
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default = 'profile_pics/wp4013910.jpg')

# adds the database that tracks accounts in chart of accounts
class AccountModel(models.Model):
    account_name = models.CharField(max_length=30, unique=True)
    account_number = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{1,10}$', 'Enter a valid number.')])
    account_description = models.CharField(max_length=150)
    normal_side = models.CharField(max_length=6)
    account_category = models.CharField(max_length=20)
    account_subcategory = models.CharField(max_length=20)
    initial_balance = models.DecimalField(max_digits=20, decimal_places=2)
    debit = models.DecimalField(max_digits=20, decimal_places=2)
    credit = models.DecimalField(max_digits=20, decimal_places=2)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    order = models.CharField(max_length=2)
    statement = models.CharField(max_length=2)
    comment = models.TextField(blank=True)
    activated = models.BooleanField()

    def __str__(self):
        return self.account_name

# adds the database that tracks journal entries
class JournalEntriesModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    account_name = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, default="pending", blank=True, null=True)

# adds the database that tracks the event logs
class EventLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateTimeField(auto_now_add=True)
    account_changed = models.CharField(max_length=30)
    before_image = models.CharField(max_length=100, null=True, blank=True)
    after_image = models.CharField(max_length=100)