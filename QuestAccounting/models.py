from django.db import models, migrations
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.forms import ModelForm
from django.contrib.auth.hashers import make_password

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
