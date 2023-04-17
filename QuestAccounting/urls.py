
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_password_reset
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # credential based urls
    path('', views.home, name = 'home'),
    path('login/', views.login_view, name = "login"),
    path('register/', views.signup, name = "register"),
    path('logout/', views.logout_view, name = "logout"),


    # admin based urls
    path('administrator/', views.admin, name = "admin"),
    path('administrator/user_creation/', views.user_creation, name = "user_creation"),
    path('administrator/user_creation/<int:user_id>/', views.group_selection, name = "group_selection"),


    # manager+ based urls
    path('manager/', views.manager, name = "manager"),
    path('user_view/', views.user_view, name = "user_view"),
    path('user_management/', views.user_management, name = "user_management"),
    path('user_view/<int:user_id>/', views.individual_user_view, name = "detailed_user"),
    path('user_view/<int:user_id>/edit_user', views.edit_user, name = "edit_user"),


    path('journals/', views.journal_entries, name = "journal_entries"),
    path('journals/view', views.view_journal_entries, name = "view_journal_entries"),
    path('journals/add', views.add_journal_entries, name = "add_journal_entries"),
    path('journals/pending', views.pending_journal_entries, name = "pending_journal_entries"),
    path('journals/all', views.all_journal_entries, name = "all_journal_entries"),
    path('journals/approve/<int:id>', views.approve_journal_entries, name = "approve_journal_entries"),
    path('journals/reject/<int:id>', views.reject_journal_entries, name = "reject_journal_entries"),


    


    # regular+ based urls
    path('regular/', views.regular, name = "regular"),
    path('account/', views.account, name = "account"),
    path('account/edit_profile_picture', views.edit_profile_picture, name = "edit_profile_picture"),
    path('help/', views.help, name = "help"),
    path('event_logs/', views.event_logs, name = "event_logs"),
    

    # password reset urls
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # account based urls
    path('view_account_list/', views.view_account_list, name = "view_account_list"),
    path('view_account_list/<str:account_name>/', views.select_account_view, name = "select_account_view"),
    path('view_accounts/', views.view_accounts, name = "view_accounts"),
    path('edit-<str:account_name>/', views.edit_accounts, name = "edit_accounts"),
    path('add_account/', views.add_accounts, name = "add_accounts"),
    path('deactivate-<str:account_name>/', views.deactivate_accounts, name = "deactivate_accounts"),
    path('view_accounts/general_ledger-<str:account_name>/', views.general_ledger, name = "general_ledger"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
