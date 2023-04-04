from django.db import models, migrations
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.forms import ModelForm
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator


class AccountRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField()


class UserCreation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField()
    username = models.CharField(max_length=30)
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    

    USERNAME_FIELD = 'username'

    def set_password(self, password):
        self.password = make_password(password)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default = 'profile_pics/wp4013910.jpg')

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

