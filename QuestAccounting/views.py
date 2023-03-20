
import logging
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationRequest, UserCreation
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.shortcuts import render
from .forms import UserCreation
from django.urls import reverse

def home(request):
    return render(request, 'QuestAccounting/dashboard.html')

# Login Based Views

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin')
                elif user.groups.filter(name='Manager').exists():
                    return redirect('manager')
                elif user.groups.filter(name='Regular').exists():
                    return redirect('regular')
    else:
        form = AuthenticationForm()
    return render(request, 'QuestAccounting/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, 'QuestAccounting/admin.html')
    pass

@login_required
@user_passes_test(lambda u: not u.is_superuser and u.groups.filter(name='Manager').exists())
def manager(request):
    return render(request, 'QuestAccounting/manager.html')
    pass

@login_required
@user_passes_test(lambda u: not u.is_superuser and u.groups.filter(name='Regular').exists())
def regular(request):
    return render(request, 'QuestAccounting/regular.html')
    pass

# Logout View
def logout_view(request):
    logout(request)
    return redirect('/')

# User Creation Request View
def signup(request):
    form = UserCreationRequest(request)

    if request.method == 'POST':
        form=UserCreationRequest(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('login')
    else: 
        form = UserCreationRequest()
       

    context = {'form':form}
    return render(request, 'QuestAccounting/signup.html', context)

# Account Settings View
def account(request):
    return render(request, 'QuestAccounting/account.html')

#Admin's User Creation View
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_creation(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if not form.is_valid():
            print(form.errors)

        if form.is_valid():
            # Save the new user object
            user = form.save()
            # Set the additional fields on the user object
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.save()

            return render(request, 'QuestAccounting/user_created.html')
        else:
            context = {'form': form}
            return render(request, 'QuestAccounting/user_creation.html', context)
    else:
        form = UserCreation(initial={})

    context = {'form': form}
    return render(request, 'QuestAccounting/user_creation.html', context)

