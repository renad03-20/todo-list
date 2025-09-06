from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'todoapp/todo.html', {})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        new_user = User.objects.create_user(username=username, 
                                           email=email, 
                                           password1=password1,
                                           password2=password2)
        new_user.save()
    return render(request, 'todoapp/register.html', {})

def loginpage (request):
    return render(request, 'todoapp/login.html', {})