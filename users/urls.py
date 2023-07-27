from django.urls import path
from . import views

urlpatterns = [
    path('register-customer/', views.register_customer, name='register-customer'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('view-users/', views.view_all_users, name='view-users'),
]