from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'inicio.html')

def show_login(request):
    return render(request,'signin.html')

def show_register(request):
    return render(request,'register.html')

def register(request):
    errors = Users.objects.validations(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/register')
    else:
        passw = request.POST['password']
        hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
        level = 5
        if not Users.objects.first():
            level = 9
        u=Users.objects.create(
                fname=request.POST['fname'], 
                lname=request.POST['lname'], 
                email=request.POST['email'], 
                fday=request.POST['date'], 
                password=hash,
                user_level=level
                )
        u.active = True
        u.save()
        if 'id' in request.session:
            return redirect('/dashboard/')
        return redirect('/signin')


def login(request):
    try:
        usuario = Users.objects.filter(email=request.POST.get('email'))
        if len(usuario) > 0:
            u = usuario[0]
            hash = u.password
            password = request.POST['password'].encode()

            if bcrypt.checkpw(password, hash.encode()):

                u.active = True
                u.save()
                request.session['id'] = u.id
                return redirect('/success')

            else:
                messages.error (request, 'Error contraseña incorrecta')
                return redirect('/signin')

        elif len(usuario) == 0:
            messages.error (request, 'Email no registrado')
            return redirect('/signin')
    except:
        return redirect('/signin')



def success_login(request):
    usuario = Users.objects.filter(id=request.session.get('id'))
    if len(usuario) > 0 :
        if usuario[0].active == True:

            usuario[0]
            context = {
                    'usuario': usuario[0].fname + ' ' + usuario[0].lname,
                    'tipo_sesion':'logueado/a', 
                    'fecha': usuario[0].create_at
                }
            if 'registrado' in request.session:
                context['tipo_sesion'] = 'registrado/a'
            return render(request, 'logged_in.html', context)
    messages.error (request,'Debe iniciar sesión o registrarse para ingresar')
    return redirect('/signin')


def validate_email(request):
    if 'email' in request.POST:
        email = request.POST.get('email')
        mail=Users.objects.filter(email=email)
        if len(mail) > 0:
            if not 'id' in request.session:
                return HttpResponse ('El Email ya se encuentra registrado')
            else:
                u= Users.objects.get(id=request.session['id'])
                if u.email != mail[0].email:
                    return HttpResponse ('El Email ya se encuentra registrado')
    return HttpResponse('')


def logout(request):
    if 'id' in request.session:
        print('si habia id: ', request.session['id'])
        try:
            c = Users.objects.get(id=request.session['id'])
            c.active = False
            c.save()
        
            request.session.flush()
            messages.error(request,'Se ha cerrado sesión de manera exitosa')
        except:
            print('error')
            pass
    else:
        print('no habia id')
    return redirect('/signin')
