from django.urls import path
from . import views

urlpatterns = [
    path('show/<int:num>', views.index, name='show'),
    path('edit', views.show_edit),
    path('update', views.edit),
    path('edit/<int:num>', views.show_edit_user),
    path('update/<int:num>', views.edit_user),
    path('post_message', views.post_message, name='post_message'),
    path('post_comment', views.post_comment, name='post_comment'),
    path('deletemsg', views.delete_msg, name='deletemsg'),
    path('deletecmt', views.delete_cmt, name='delete_cmt'),
    path('content/<int:num>', views.content),
]