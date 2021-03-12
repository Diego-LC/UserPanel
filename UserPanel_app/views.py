from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from session_register_app.models import *



def index_admin(request):
    val = request.session.get('id')
    try:
        u = Users.objects.filter(id=request.session.get('id'))[0]
        if u.user_level == 9:
            if Users.objects.isActive(val):
                context = {
                    'usuario': Users.objects.get(id=val),
                    'usuarios': Users.objects.all()
                }
                return render(request, 'dashboard.html', context)
        return redirect('/signin')
    except:
        messages.error (request, 'Debe registrase o iniciar sesión primero')
        print('error index')
        return redirect('/signin')

def index(request):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    if u:
        if u[0].user_level == 9:
            return redirect('/dashboard/admin')
    if Users.objects.isActive(val):
        context = {
            'usuario': Users.objects.get(id=val),
            'usuarios': Users.objects.all()
        }
        return render(request, 'dashboard.html', context)
    return redirect('/signin')


def show_add_new_user(request):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    if u:
        user = u[0]
        if user.user_level == 9:
            return render(request,'add_user.html')
    return redirect('/dashboard')


def delete_user(request, num):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    d = Users.objects.filter(id=num)
    if u and d:
        if u[0].user_level == 9:
            delete = d[0]
            delete.delete()
        return redirect('/dashboard')
    return redirect('/signin')

