from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('admin', views.index_admin),
    path('add_user', views.show_add_new_user, name='add_user'),
    path('destroy/<int:num>', views.delete_user),
]