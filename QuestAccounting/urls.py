
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    # credential based urls
    path('', views.home, name = 'home'),
    path('login/', views.login_view, name = "login"),
    path('register/', views.signup, name = "register"),
    path('logout/', views.logout_view, name = "logout"),


    #admin based urls
    path('administrator/', views.admin, name = "admin"),
    path('administrator/user_creation/', views.user_creation, name = "user_creation"),


    #manager+ based urls
    path('manager/', views.manager, name = "manager"),
    path('user_view/', views.user_view, name = "user_view"),
    path('user_view/<int:user_id>/', views.individual_user_view, name = "detailed_user"),
    path('user_view/<int:user_id>/edit_user', views.edit_user, name = "edit_user"),


    #regular+ based urls
    path('regular/', views.regular, name = "regular"),
    path('account/', views.account, name = "account"),
    

    
    


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
