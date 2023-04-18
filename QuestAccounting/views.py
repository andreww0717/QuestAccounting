
from base64 import urlsafe_b64encode
from gettext import translation
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.dispatch import Signal
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from QuestAccounting.models import AccountModel, AllJournalEntriesModel, EventLog, JournalEntriesModel, PendingJournalEntriesModel, RejectedJournalEntriesModel, UserProfile
from .forms import AllJournalEntriesForm, EmailForm, GroupSelection, PendingJournalEntriesForm, RejectedJournalEntriesForm, UserCreationRequest, UserCreation, UserProfileForm, userList, EditUser, PasswordReset, AccountForm, JournalEntriesForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from .signals import account_changed
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.db import transaction

# original login page 
def home(request):
    return render(request, 'QuestAccounting/dashboard.html')

# help page View
def help(request):
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    return render(request, 'QuestAccounting/help/help.html', context)

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
                if user.groups.filter(name='Admin').exists():
                    return redirect('admin')
                elif user.groups.filter(name='Manager').exists():
                    return redirect('manager')
                elif user.groups.filter(name='Regular').exists():
                    return redirect('regular')
    else:
        form = AuthenticationForm()
    return render(request, 'QuestAccounting/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def admin(request):
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    
    return render(request, 'QuestAccounting/admin.html', context)
    pass

@login_required
@user_passes_test(lambda u: not u.groups.filter(name='Admin').exists() and u.groups.filter(name='Manager').exists())
def manager(request):
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    return render(request, 'QuestAccounting/manager.html', context)
    pass

@login_required
@user_passes_test(lambda u: not u.groups.filter(name='Admin').exists() and u.groups.filter(name='Regular').exists())
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











# User Management View
def user_management(request):
    context = {
        'is_superuser': request.user.is_superuser,
        'groups': request.user.groups.values_list('name', flat=True),  
    }
    return render(request, 'QuestAccounting/user_management.html', context)











# Admin's User Creation View
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
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
            return redirect('group_selection', user_id = user.id)
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

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def group_selection(request, user_id):

    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        form = GroupSelection(request.POST)

        if not form.is_valid():
            print(form.errors)
        
        if form.is_valid():
            group_name = form.cleaned_data.get('group')
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            user.save()
        context = {'user': user,  
                   'form': form,
                   'is_superuser': request.user.is_superuser,
                   'groups': request.user.groups.values_list('name', flat=True),
                    }
        return render(request, 'QuestAccounting/user_created.html', context)
    else:
        user = get_object_or_404(User, id=user_id)
        form = GroupSelection(request.POST)
        context = {'user': user,  
                   'form': form,
                   'is_superuser': request.user.is_superuser,
                   'groups': request.user.groups.values_list('name', flat=True),
                    }
        return render(request, 'QuestAccounting/group_selection.html', context)










# User Viewing Views

@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Manager').exists() and not u.groups.filter(name='Regular').exists())
def user_view(request):
    userList = User.objects.all()
    context = {'userList': userList,
               'is_superuser': request.user.is_superuser,
               'groups': request.user.groups.values_list('name', flat=True),
               }
    return render(request, 'QuestAccounting/user_view.html', context)

@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Manager').exists() and not u.groups.filter(name='Regular').exists())
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
            
            context = {'previous_page': previous_page, 
                       'user': user, 'form': form, 
                       'is_superuser': request.user.is_superuser, 
                       'groups': request.user.groups.values_list('name', flat=True),
                       }
            print(previous_page)
            if previous_page == 'http://127.0.0.1:8000/account/':
                return redirect('account')
            else: 
                return redirect('detailed_user', user_id)
        else:
            
            context = {'previous_page': previous_page, 
                       'user': user, 'form': form, 
                       'is_superuser': request.user.is_superuser, 
                       'groups': request.user.groups.values_list('name', flat=True),
                       }

            return render(request, 'QuestAccounting/edit_user.html', context)
    else:
        form = EditUser(instance=user)
        previous_page = request.META.get('HTTP_REFERER')
        request.session['previous_page'] = previous_page
        print(previous_page)
        form.fields['previous_page'] = forms.CharField(widget=forms.HiddenInput(), initial=previous_page)
        context = {'previous_page': previous_page, 
                   'user': user, 'form': form, 
                   'is_superuser': request.user.is_superuser, 
                   'groups': request.user.groups.values_list('name', flat=True),
                   }

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
    
    context = {'user': user, 
               'form': form, 
               'groups': request.user.groups.values_list('name', flat=True), 
               'is_superuser': request.user.is_superuser
               }
    return render(request, 'QuestAccounting/edit_profile_picture.html', context)










# Account Views

def view_accounts(request):
    user = request.user
    account_info = AccountModel.objects.all()
    form = AccountForm()
    context = {'form': form, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True), 
               'user': user, 
               'account_info': account_info
               }
    return render(request, 'QuestAccounting/chartofaccounts/view_accounts.html', context)

def edit_accounts(request, account_name):
    user = request.user
    account_info = AccountModel.objects.all()
    previous_page = request.session.get('previous_page', None)
    account = get_object_or_404(AccountModel, account_name=account_name)
    if request.method == 'POST':
        
        print(previous_page)
        form = AccountForm(request.POST, instance=account)
        context = {'previous_page': previous_page, 
                   'user': user, 
                   'form': form, 
                   'is_superuser': request.user.is_superuser, 
                   'groups': request.user.groups.values_list('name', flat=True), 
                   'account': account, 
                   'account_info': account_info
                   }
        if form.is_valid():
            print(form.errors)
            print('form is valid')
            account_changed.send(sender=AccountModel, user=request.user, instance=account, new=False)
            form.save()
            
            if previous_page == 'view_account_list':
                return redirect(select_account_view, account.account_name)
            else:
                return redirect(view_accounts)
    else:
        form = AccountForm(instance=account)
        referer = request.META.get('HTTP_REFERER')
        previous_page = referer.split('/')[3]
        request.session['previous_page'] = previous_page
        context = {'previous_page': previous_page, 
                   'user': user, 
                   'form': form, 
                   'account': account, 
                   'groups': request.user.groups.values_list('name', flat=True), 
                   'is_superuser': request.user.is_superuser
                   }
        return render(request, 'QuestAccounting/chartofaccounts/edit_accounts.html', context)
    
    

def add_accounts(request):
    user = request.user
    form = AccountForm(request.POST)
    
    print(request.method)
    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.activated = True
            account.save()
            account_changed.send(sender=AccountModel, user=request.user, instance=account, new=True)
            return redirect(view_accounts)
        else:
            print(form.errors)
            context = {'form': form, 
                       'is_superuser': request.user.is_superuser, 
                       'user': user
                       }
            return render(request, 'QuestAccounting/chartofaccounts/add_accounts.html', context)
    else:
        context = {'form': form, 
                   'is_superuser': request.user.is_superuser, 
                   'user': user
                   }
        return render(request, 'QuestAccounting/chartofaccounts/add_accounts.html', context)


def deactivate_accounts(request, account_name):
    user = request.user
    account_info = AccountModel.objects.all()
    account = get_object_or_404(AccountModel, account_name=account_name)
    print(account_name)
    print(request.method)
    
    if request.method == 'POST':
        print(request.method)
        form = AccountForm(request.POST, instance=account)
        context = {'user': user, 
                   'form': form, 
                   'is_superuser': request.user.is_superuser, 
                   'account': account, 
                   'account_info': account_info, 
                   'groups': request.user.groups.values_list('name', flat=True)
                   }
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, 'QuestAccounting/chartofaccounts/view_accounts.html', context)
    else:
        
        form = AccountForm(instance=account)
    context = {'user': user, 
               'form': form, 
               'account': account, 
               'is_superuser': request.user.is_superuser
               }
    return render(request, 'QuestAccounting/chartofaccounts/deactivate_accounts.html', context)

def view_account_list(request):
    user = request.user
    account_info = AccountModel.objects.all()
    context = {'user': user, 
               'is_superuser': request.user.is_superuser, 
               'account_info': account_info, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/chartofaccounts/view_account_list.html", context)

def select_account_view(request, account_name):
    user = request.user
    account_info = AccountModel.objects.all()
    account = get_object_or_404(AccountModel, account_name=account_name)
    context = {'user': user, 
               'is_superuser': request.user.is_superuser, 
               'account': account, 
               'account_info': account_info, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/chartofaccounts/select_account_view.html", context)









# General Ledger View
def general_ledger(request, account_name):
    user = request.user
    account_info = AccountModel.objects.all()
    account = get_object_or_404(AccountModel, account_name=account_name)
    context = {'user': user, 
               'is_superuser': request.user.is_superuser, 
               'account': account, 
               'account_info': account_info, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/general_ledger.html", context)











# Event Logs View
def event_logs(request):
    user = request.user
    event_logs = EventLog.objects.all()
    context = {'user': user, 
               'is_superuser': request.user.is_superuser, 
               'event_logs': event_logs, 
               'account': account, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, 'QuestAccounting/event_logs.html', context)









# Journal Entries Views

def journal_entries(request):
    user = request.user
    total_credit = JournalEntriesModel.objects.aggregate(Sum('credit'))['credit__sum']
    total_debit = JournalEntriesModel.objects.aggregate(Sum('debit'))['debit__sum']
    if total_credit == total_debit:
        doTheyMatch = True
    else:
        doTheyMatch = False
    context = {'user': user, 
               'doTheyMatch': doTheyMatch, 
               'total_credit': total_credit, 
               'total_debit': total_debit, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/journalentries/journal_entries.html", context)

def view_journal_entries(request):
    user = request.user
    journal_entries = JournalEntriesModel.objects.all()

    total_credit = JournalEntriesModel.objects.aggregate(Sum('credit'))['credit__sum']
    total_debit = JournalEntriesModel.objects.aggregate(Sum('debit'))['debit__sum']
    if total_credit == total_debit:
        doTheyMatch = True
    else:
        doTheyMatch = False
    context = {'user': user, 
               'journal_entries': journal_entries, 
               'doTheyMatch': doTheyMatch, 
               'total_credit': total_credit, 
               'total_debit': total_debit, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/journalentries/view_journal_entries.html", context)

def add_journal_entries(request):
    user = request.user
    form = JournalEntriesForm(request.POST)
    accountant_form = PendingJournalEntriesForm(request.POST)
    all_form = AllJournalEntriesForm(request.POST)
    total_credit = JournalEntriesModel.objects.aggregate(Sum('credit'))['credit__sum']
    total_debit = JournalEntriesModel.objects.aggregate(Sum('debit'))['debit__sum']
    if total_credit == total_debit:
        doTheyMatch = True
    else:
        doTheyMatch = False
    context = {'user': user, 
               'form': form, 
               'doTheyMatch': doTheyMatch, 
               'total_credit': total_credit, 
               'total_debit': total_debit, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    if request.method == 'POST':
        if form.is_valid():
            journal_entry = form.save(commit=False)
            if 'Regular' in request.user.groups.values_list('name', flat=True):
                journal_entry.status = 'pending'
                accountant_form.save()
                all_form.save()
            elif  'Manager' in request.user.groups.values_list('name', flat=True) or 'Admin' in request.user.groups.values_list('name', flat=True):
                journal_entry.status = 'approved'
                form.save()
                with transaction.atomic():
                    accountant_entry = accountant_form.save(commit=False)
                    accountant_entry.save()
                    accountant_entry.delete()
                all_form.save()

            return redirect(journal_entries)

    
    return render(request, "QuestAccounting/journalentries/add_journal_entries.html", context)

def pending_journal_entries(request):
    user = request.user
    pending_journal_entries = PendingJournalEntriesModel.objects.all()
    total_credit = JournalEntriesModel.objects.aggregate(Sum('credit'))['credit__sum']
    total_debit = JournalEntriesModel.objects.aggregate(Sum('debit'))['debit__sum']
    if total_credit == total_debit:
        doTheyMatch = True
    else:
        doTheyMatch = False
    context = {'user': user, 
               'pending_journal_entries': pending_journal_entries,
               'doTheyMatch': doTheyMatch, 
               'total_credit': total_credit, 
               'total_debit': total_debit, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/journalentries/pending_journal_entries.html", context)

def all_journal_entries(request):
    user = request.user
    all_journal_entries = AllJournalEntriesModel.objects.all()
    total_credit = JournalEntriesModel.objects.aggregate(Sum('credit'))['credit__sum']
    total_debit = JournalEntriesModel.objects.aggregate(Sum('debit'))['debit__sum']
    if total_credit == total_debit:
        doTheyMatch = True
    else:
        doTheyMatch = False
    context = {'user': user, 
               'all_journal_entries': all_journal_entries,
               'doTheyMatch': doTheyMatch, 
               'total_credit': total_credit, 
               'total_debit': total_debit, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/journalentries/all_journal_entries.html", context)

def journal_entry_approval(request, id):
    user = request.user
    journal_entry = AllJournalEntriesModel.objects.get(id=id)
    pending_entry = PendingJournalEntriesModel.objects.get(id=id)
    if 'approved' in request.POST:
            journal_entry.status = "approved"
    if 'rejected' in request.POST:
            journal_entry.status = "rejected"

    form = JournalEntriesForm(instance=journal_entry)
    total_credit = JournalEntriesModel.objects.aggregate(Sum('credit'))['credit__sum']
    total_debit = JournalEntriesModel.objects.aggregate(Sum('debit'))['debit__sum']
    if total_credit == total_debit:
        doTheyMatch = True
    else:
        doTheyMatch = False

    
    if request.method == 'POST':
        form = JournalEntriesForm(request.POST, instance=journal_entry)
        form = RejectedJournalEntriesForm(request.POST, instance=journal_entry)  
        
        if form.is_valid():
            if 'approved' in request.POST:
                journal_entry_model = JournalEntriesModel.objects.create(
                account_name=form.cleaned_data['account_name'],
                debit=form.cleaned_data['debit'],
                credit=form.cleaned_data['credit']
                )
                
            if 'rejected' in request.POST:
                journal_entry_model = RejectedJournalEntriesModel.objects.create(
                account_name=form.cleaned_data['account_name'],
                debit=form.cleaned_data['debit'],
                credit=form.cleaned_data['credit']
                )
            journal_entry.save()
            journal_entry_model.save()
            pending_entry.delete()

            return redirect(journal_entries)

    context = {'user': user, 
               'form': form,
               'journal_entry': journal_entry,
               'doTheyMatch': doTheyMatch, 
               'total_credit': total_credit, 
               'total_debit': total_debit, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/journalentries/journal_entry_approval.html", context)















# Email User View

def email_user(request):
    user = request.user
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            recipient = User.objects.get(username=recipient_username)
            recipient_email = recipient.email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email = EmailMessage(
                subject=subject,
                body=message,
                to=[recipient_email]
            )
            email.send()

            messages.success(request, 'Email sent successfully!')
            return redirect('view_accounts')
    else:
        form = EmailForm()

    context = {'user': user, 
               'form': form, 
               'is_superuser': request.user.is_superuser, 
               'groups': request.user.groups.values_list('name', flat=True)
               }
    return render(request, "QuestAccounting/email_user.html", context)
