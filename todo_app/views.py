from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Task  

# Create your views here.
def home(request):
    if request.method == 'POST':
        task_content = request.POST.get('task')#!gets the task from the form 

        if task_content:
            Task.objects.create(task=task_content)#! create and save new task to database

        return redirect('home-page')
    
    tasks = Task.objects.all()

    return render(request, 'todoapp/todo.html', { 'tasks': tasks })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        if len(password) < 3:
            messages.error(request, 'password must be it leasr three characters')
            return redirect('register')

        new_user = User.objects.create_user(username=username, 
                                           email=email, 
                                           password=password)
        new_user.save()
    return render(request, 'todoapp/register.html', {})

def loginpage (request):
    return render(request, 'todoapp/login.html', {})