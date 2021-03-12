from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
import datetime 
from django.utils import timezone

def show_edit(request):
    if 'id' in request.session:
        val = request.session.get('id')
        u = Users.objects.filter(id=val)
        if u:
            context = {
                'user': u[0],
            }
            return render(request,'edit.html', context)
    return redirect('/signin')

def show_edit_user(request, num):
    if 'id' in request.session:
        admin = Users.objects.get(id=request.session['id'])
        u = Users.objects.filter(id=num)
        if u and admin.user_level == 9:
            context = {
                'user': u[0],
            }
            return render(request,'edit_users.html', context)
        return redirect('/dashboard')
    return redirect('/signin')


def edit(request):
    if 'id' in request.session:
        val = request.session.get('id')
        u = Users.objects.filter(id=val)
        if u and request.POST:
            errors = Users.objects.validations(request.POST)
            if len(errors) > 0:
                for key, val2 in errors.items():
                    messages.error(request, val2)
                return redirect(f'/user/edit')
            
            user = u[0]
            if 'email' in request.POST:
                user.email = request.POST['email']
                user.fname = request.POST['fname']
                user.lname = request.POST['lname']
                user.save()
                messages.error(request, 'Perfil actualizado')

            if 'password' in request.POST:
                passw = request.POST['password']
                hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
                user.password = hash
                user.save()
                messages.error(request, 'Contraseña actualizada')

            if 'desc' in request.POST:
                user.desc = request.POST['desc']
                user.save()
                messages.error(request, 'Perfil actualizado')

        return redirect('/user/edit')
    return redirect('/signin')

def edit_user(request, num):
    if 'id' in request.session:
        admin = Users.objects.get(id=request.session['id'])
        u = Users.objects.filter(id=num)
        if u and request.POST and admin.user_level == 9:
            errors = Users.objects.validations(request.POST)
            if len(errors) > 0:
                for key, val2 in errors.items():
                    messages.error(request, val2)
                return redirect(f'/user/edit/{num}')
            
            user = u[0]
            if 'email' in request.POST:
                user.email = request.POST['email']
                user.fname = request.POST['fname']
                user.lname = request.POST['lname']
                user.user_level = request.POST['level']
                user.save()
                messages.error(request, 'Perfil actualizado')

            if 'password' in request.POST:
                passw = request.POST['password']
                hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
                user.password = hash
                user.save()
                messages.error(request, 'Contraseña actualizada')

            return redirect(f'/user/edit/{num}')
    return redirect('/signin')


def isValid(val):
    usuario = Users.objects.filter(id=val)
    if len(usuario) > 0 :
        user = usuario[0]
        if user.active == True:
            return True
    return False

def index(request, num):
    id=request.session.get('id')
    usuario = Users.objects.filter(id=id)
    user = Users.objects.filter(id=num)
    if isValid(id):
        if user:
            context = {
                    'user': user[0],
                }
            return render(request, 'muro.html', context)
        return redirect('/dashboard')
    messages.error (request,'Debe iniciar sesión o registrarse primero')
    return redirect('/signin')


def content(request, num):
    id=request.session.get('id')
    usuario = Users.objects.filter(id=id)
    if isValid(id):
        user = usuario[0]
        context = {
                'usuario': user,
                'mensajes': Messages.objects.filter(user_msg__id=num),
                'since_msg':[],
                'since_comm': []
            }
        for m in context['mensajes']:
            if (timezone.now() - m.create_at) < datetime.timedelta(minutes=300):
                print ('mensaje creado hace menos de 300 min', m.create_at)
                context['since_msg'].append(m.id)
            for c in m.comments.all():
                if (timezone.now() - c.create_at) < datetime.timedelta(minutes=300):
                    print ('comentario creado hace menos de 300 min', c.create_at)
                    context['since_comm'].append(c.id)
        # print(context['delete'])
        return render(request, 'content.html', context)
    messages.error (request,'Debe iniciar sesión o registrarse primero')
    return redirect('/signin')


def post_message(request):
    val = request.session.get('id')
    print('id: ', request.POST['id_user'])
    if isValid(val):
        u_from = Users.objects.get(id=val)
        user_to = Users.objects.get(id=request.POST['id_user'])
        Messages.objects.create(
            user_msg=user_to, 
            who_sent=u_from, 
            message=request.POST.get('post_message')
        )
    return redirect(f'/user/content/{request.POST["id_user"]}')


def post_comment(request):
    val = request.session.get('id')
    if isValid(val):
        print(request.POST.get('post_msg'))
        u = Users.objects.get(id=val)
        m = Messages.objects.get(id=request.POST.get('id_msg'))
        Comments.objects.create(who_comment=u, message_com=m, comment=request.POST.get('post_comment'))
        return redirect(f'/user/content/{request.POST["id_user"]}')
    return redirect('/dashboard')


def delete_msg(request):
    val = request.session.get('id')
    if isValid(val):
        print(request.POST.get('id_mes'))

        u = Users.objects.get(id=val)
        m = Messages.objects.get(id=request.POST.get('id_mes'))
        # if (timezone.now() - m.create_at) < datetime.timedelta(minutes=30):
        m.delete()
        
        return redirect(f'/user/content/{request.POST.get("id_user")}')
    return redirect('/dashboard')

def delete_cmt(request):
    val = request.session.get('id')
    if isValid(val):
        # print(request.POST.get('id_msg'))

        u = Users.objects.get(id=val)
        c = Comments.objects.get(id=request.POST.get('id_cmt'))
        c.delete()
        return redirect(f'/user/content/{request.POST.get("id_user")}')
    return redirect('/dashboard')
