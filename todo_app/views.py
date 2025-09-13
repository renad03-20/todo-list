from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task 
from django.http import JsonResponse
import json

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        task_content = request.POST.get('task')#!gets the task from the form 

        if task_content:
            Task.objects.create(task=task_content, user=request.user)#! create and save new task to database
        return redirect('home-page')
    
    tasks = Task.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todoapp/todo.html', { 'tasks': tasks })

@login_required
def toggle_complete(request):
    """Toggle a task's completion (AJAX)"""
    if request.method == "POST":
        data = json.loads(request.body)  # Parse JSON body
        task_id = data.get('id')

        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.completed = not task.completed
            task.save()
            return JsonResponse({'success': True, 'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def delete_task_ajax(request):
    """Delete a task (AJAX)"""
    if request.method == "POST":
        data = json.loads(request.body)  # Parse JSON body
        task_id = data.get('id')

        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'password must be it leasr three characters')
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'username already exist, use another one!')
            return redirect('register')

        new_user = User.objects.create_user(username=username, 
                                           email=email, 
                                           password=password)
        new_user.save()

        messages.success(request, 'user successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def loginpage (request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #!check the database to see if the user exist, return none if not 
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
        
    return render(request, 'todoapp/login.html', {})

def logoutpage(request):
    logout(request)
    return redirect('login')