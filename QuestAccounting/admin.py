from django.contrib import admin
from .models import AccountRequest, AllJournalEntriesModel, PendingJournalEntriesModel, RejectedJournalEntriesModel, UserProfile, AccountModel, JournalEntriesModel, JournalEntryDocuments, EventLog

# Register your models here.

# adds these models to the django admin page

class AccountRequestAdmin(admin.ModelAdmin):
     list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'email', 'user_id')

admin.site.register(AccountRequest, AccountRequestAdmin)


class UserProfileAdmin(admin.ModelAdmin):
     list_display = ('id','user_id', 'profile_pic')

admin.site.register(UserProfile, UserProfileAdmin)


class AccountModelAdmin(admin.ModelAdmin):
     list_display = ('id', 'account_name', 'account_number', 'debit', 'credit', 'balance', 'activated')

admin.site.register(AccountModel, AccountModelAdmin)


class JournalEntriesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'debit', 'credit', 'status', 'account_name_id')

admin.site.register(JournalEntriesModel, JournalEntriesModelAdmin)


class PendingJournalEntriesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'debit', 'credit', 'status', 'account_name_id')

admin.site.register(PendingJournalEntriesModel, PendingJournalEntriesModelAdmin)


class RejectedJournalEntriesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'debit', 'credit', 'status', 'account_name_id', 'comment')

admin.site.register(RejectedJournalEntriesModel, RejectedJournalEntriesModelAdmin)


class AllJournalEntriesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'debit', 'credit', 'status', 'account_name_id', 'comment')

admin.site.register(AllJournalEntriesModel, AllJournalEntriesModelAdmin)

class JournalEntryDocumentsAdmin(admin.ModelAdmin):
    list_display = ('journal_entry', 'file_document', 'image_document')

admin.site.register(JournalEntryDocuments, JournalEntryDocumentsAdmin)


class EventLogAdmin(admin.ModelAdmin):
     list_display = ('id','event_date', 'before_image', 'after_image', 'user_id', 'account_changed')

admin.site.register(EventLog, EventLogAdmin)

