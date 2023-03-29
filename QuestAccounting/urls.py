
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


    # manager+ based urls
    path('manager/', views.manager, name = "manager"),
    path('user_view/', views.user_view, name = "user_view"),
    path('user_view/<int:user_id>/', views.individual_user_view, name = "detailed_user"),
    path('user_view/<int:user_id>/edit_user', views.edit_user, name = "edit_user"),


    # regular+ based urls
    path('regular/', views.regular, name = "regular"),
    path('account/', views.account, name = "account"),
    path('account/edit_profile_picture', views.edit_profile_picture, name = "edit_profile_picture"),
    

    # password reset urls
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # account based urls
    path('account_homepage/', views.account_homepage, name = "account_homepage"),
    path('account_homepage/view', views.view_accounts, name = "view_accounts"),
    path('account_homepage/edit', views.edit_accounts, name = "edit_accounts"),
    path('account_homepage/add', views.add_accounts, name = "add_accounts"),
    path('account_homepage/deactivate', views.deactivate_accounts, name = "deactivate_accounts"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
