from django.contrib import admin
from .models import AccountRequest, UserProfile, AccountModel, JournalEntriesModel, EventLog

# Register your models here.

# adds these models to the django admin page
admin.site.register(AccountRequest)
admin.site.register(UserProfile)
admin.site.register(AccountModel)
admin.site.register(JournalEntriesModel)
admin.site.register(EventLog)