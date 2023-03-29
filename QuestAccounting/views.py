
from base64 import urlsafe_b64encode
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

from QuestAccounting.models import AccountModel, UserProfile
from .forms import UserCreationRequest, UserCreation, UserProfileForm, userList, EditUser, PasswordReset, AccountForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.shortcuts import render
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
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    
    return render(request, 'QuestAccounting/admin.html', context)
    pass

@login_required
@user_passes_test(lambda u: not u.is_superuser and u.groups.filter(name='Manager').exists())
def manager(request):
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    return render(request, 'QuestAccounting/manager.html', context)
    pass

@login_required
@user_passes_test(lambda u: not u.is_superuser and u.groups.filter(name='Regular').exists())
def regular(request):
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    return render(request, 'QuestAccounting/regular.html', context)
    pass

# Logout View
def logout_view(request):
    logout(request)
    return redirect('/')

# Password Reset View
def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordReset(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='QuestAccounting/txt/passwordresetsubject.txt',
            )
            return render(request, 'QuestAccounting/Password Reset/password_reset_done.html')
    else:
        form = PasswordReset()
    return render(request, 'QuestAccounting/Password Reset/password_reset_form.html', {'form': form})

# def custom_password_reset_done(request):


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
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    return render(request, 'QuestAccounting/account.html', context)

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
            context = {'form': form, 
                       'is_superuser': request.user.is_superuser,
                       'groups': request.user.groups.values_list('name', flat=True),
                    }
            return render(request, 'QuestAccounting/user_creation.html', context)
    else:
        form = UserCreation(initial={})

    context = {'form': form, 
                'is_superuser': request.user.is_superuser,
                'groups': request.user.groups.values_list('name', flat=True),
                    }
    return render(request, 'QuestAccounting/user_creation.html', context)

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Manager').exists() and not u.groups.filter(name='Regular').exists())
def user_view(request):
    userList = User.objects.all()
    context = {'userList': userList,
               'is_superuser': request.user.is_superuser,
               'groups': request.user.groups.values_list('name', flat=True),
               }
    return render(request, 'QuestAccounting/user_view.html', context)

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Manager').exists() and not u.groups.filter(name='Regular').exists())
def individual_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {'user': user,
               'is_superuser': request.user.is_superuser,
               'groups': request.user.groups.values_list('name', flat=True),
               }
    return render(request, 'QuestAccounting/individual_user_view.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    

    if request.method == 'POST':
        form = EditUser(request.POST, instance=user)
        previous_page = request.session.get('previous_page', None)
        if form.is_valid():
            form.save()
            
            context = {'previous_page': previous_page, 'user': user, 'form': form, 'is_superuser': request.user.is_superuser, 'groups': request.user.groups.values_list('name', flat=True),}
            print(previous_page)
            if previous_page == 'http://127.0.0.1:8000/account/':
                return render(request, 'QuestAccounting/account.html', context)
            else: 
                return render(request, 'QuestAccounting/individual_user_view.html', context)
        else:
            
            context = {'previous_page': previous_page, 'user': user, 'form': form, 'is_superuser': request.user.is_superuser, 'groups': request.user.groups.values_list('name', flat=True),}

            return render(request, 'QuestAccounting/edit_user.html', context)
    else:
        form = EditUser(instance=user)
        previous_page = request.META.get('HTTP_REFERER')
        request.session['previous_page'] = previous_page
        print(previous_page)
        form.fields['previous_page'] = forms.CharField(widget=forms.HiddenInput(), initial=previous_page)
        context = {'previous_page': previous_page, 'user': user, 'form': form, 'is_superuser': request.user.is_superuser, 'groups': request.user.groups.values_list('name', flat=True),}

        return render(request, 'QuestAccounting/edit_user.html', context)
    
def edit_profile_picture(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'QuestAccounting/edit_profile_picture.html', {'user': user, 'form': form, 'is_superuser': request.user.is_superuser})

def account_homepage(request):
    user = request.user
    context = {'is_superuser': request.user.is_superuser, 'user': user}
    return render(request, 'QuestAccounting/chartofaccounts/account_homepage.html', context)

def view_accounts(request):
    user = request.user
    account_info = AccountModel.objects.all()
    form = AccountForm()
    context = {'form': form, 'is_superuser': request.user.is_superuser, 'user': user, 'account_info': account_info}
    return render(request, 'QuestAccounting/chartofaccounts/view_accounts.html', context)

def edit_accounts(request):
    user = request.user
    form = AccountForm(request.POST)
    context = {'form': form, 'is_superuser': request.user.is_superuser, 'user': user}
    return render(request, 'QuestAccounting/chartofaccounts/edit_accounts.html', context)

def add_accounts(request):
    user = request.user
    form = AccountForm(request.POST)
    
    print(request.method)
    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.activated = True  # Set activated as True
            account.save()
            context = {'is_superuser': request.user.is_superuser, 'user': user}
            return render(request, 'QuestAccounting/chartofaccounts/account_homepage.html', context)
        else:
            print(form.errors)
            context = {'form': form, 'is_superuser': request.user.is_superuser, 'user': user}
            return render(request, 'QuestAccounting/chartofaccounts/add_accounts.html', context)
    else:
        context = {'form': form, 'is_superuser': request.user.is_superuser, 'user': user}
        return render(request, 'QuestAccounting/chartofaccounts/add_accounts.html', context)


def deactivate_accounts(request):
    user = request.user
    form = AccountForm(request.POST)
    context = {'form': form, 'is_superuser': request.user.is_superuser, 'user': user}
    return render(request, 'QuestAccounting/chartofaccounts/deactivate_accounts.html', context)