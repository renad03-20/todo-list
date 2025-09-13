from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('toggle_complete/', views.toggle_complete, name='toggle_complete_ajax'),
    path('delete_task/', views.delete_task_ajax, name='delete_task_ajax'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
]
