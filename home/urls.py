#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login, name="login"),
    #path('doctorlogin', views.doctorlogin, name="doctorlogin"),
    path('doctor', views.doctor, name="doctor"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('appointment', views.appointment, name='appointment'),
    path('myappointments', views.myappointments, name='myappointments'),
    path('edit', views.edit, name='edit'),
]
