from __future__ import unicode_literals
from django.db import models
import re
import datetime

class validacion(models.Manager):
    def validations(self, postData):
        errors = {}
        if postData:
            if postData.get('fname'):
                if len(postData.get('fname')) < 2 and len(postData.get('lname')) < 2:
                    errors['nombre'] = 'El campo nombre y el campo apellido deberían ser de al menos 2 carácteres'
            
            if postData.get('email'):
                EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
                mail = Users.objects.filter(email=postData['email'])
                if len(postData.get('email')) > 0:
                    if not EMAIL_REGEX.match(postData['email']):
                        errors['email'] = "El formato de email no es válido!"
                    if len(mail) > 0:
                        if 'password' in postData:
                            errors['email'] = 'Ya exite alguien registrado con el mismo email'
                else:
                    errors['email'] = 'El campo email no debería estar vacío'
            
            if postData.get('password'):
                if len(postData.get('password')) < 8:
                    errors['lenpw'] = 'La contraseña dería ser de al menos 8 carácteres'
            
                if postData.get('password') != postData.get('password2'):
                    errors['password'] = 'Las contraseñas no coinciden'
            
            if postData.get('desc'):
                if len(postData.get('desc')) < 2:
                    errors['desc'] = 'La descripción debería ser de al menos 2 carácteres'
                if len(postData.get('desc')) > 10000:
                    errors['desc'] = 'La descripción no debería superar 10 mil carácteres'
            
            if postData.get('date'):
                date = datetime.datetime.strptime(postData['date'], "%Y-%m-%d")
                now = datetime.datetime.now()
                if now <= date:
                    errors['date'] = 'La fecha de nacimento debe estar en pasado'
                if now - date < datetime.timedelta(days=4745):
                    errors['date'] = 'Deberías tener al menos 13 años para registrarte'
            
            return errors
        errors['error'] = 'Debe registrarse o loguearse primero'
        return errors

    def isActive(self, data):
        usuario = Users.objects.filter(id=data)
        if len(usuario) > 0 :
            user = usuario[0]
            if user.active == True:
                return True
        return False

class Users(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    fday = models.CharField(max_length=255)
    desc = models.TextField(null=True)
    active = models.BooleanField(default=False)
    user_level = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255)
    objects = validacion()
    #messages => user_msg
    #msg_sent => who_sent
    #msg_commenteds => who_comment

