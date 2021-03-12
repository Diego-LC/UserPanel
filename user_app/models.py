from django.db import models
from session_register_app.models import Users

class Messages(models.Model):
    user_msg = models.ForeignKey(Users, related_name='messages', on_delete = models.CASCADE)
    who_sent= models.ForeignKey(Users, related_name='msg_sent', on_delete = models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #comments => message_com

class Comments(models.Model):
    message_com = models.ForeignKey(Messages, related_name='comments', on_delete = models.CASCADE)
    who_comment = models.ForeignKey(Users, related_name='msg_commenteds', on_delete = models.CASCADE)
    comment = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)