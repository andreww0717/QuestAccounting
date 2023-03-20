from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.forms import ModelForm
from django.contrib.auth.hashers import make_password

# Create your models here.

class AccountRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)


class UserCreation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField()
    username = models.CharField(max_length=30)
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def set_password(self, password):
        self.password = make_password(password)




    