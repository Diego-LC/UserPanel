from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signin/', views.show_login),
    path('register/', views.show_register),
    path('register/reg', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('success', views.success_login),
    path('valid', views.validate_email),
]