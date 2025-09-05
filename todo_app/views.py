from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'todoapp/todo.html', {})

def register(request):
    return render(request, 'todoapp/register.html', {})

def loginpage (request):
    return render(request, 'todoapp/login.html', {})