from .models import Appointments
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import login as kishore, authenticate, logout


def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            messages.error(request, 'Passwords Doesn\'t match')
            return render(request, 'home/register.html')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'home/register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'home/register.html')
        else:
            user = User.objects.create_user(
                username=username, password=password1, email=email)
            user.save()
            return redirect("login")
        return render(request, 'home/register.html')
    return render(request, 'home/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            kishore(request, user)
            return redirect('/', {
                'key': user.id
            })
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'home/login.html')

    else:
        return render(request, 'home/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def index(request):
    apps = Appointments.objects.filter(status=1)
    return render(request, "home/index.html", {'apps': apps})


def appointment(request):
    if request.method == "POST":
        appointment_time = request.POST["app_time"]
        appointment_date = request.POST["app_date"]
        appointment_description = request.POST["app_des"]
        #phone_number = request.POST["phone_number"]
        user_id = request.POST["user_id"]
        appointment = Appointments(appointment_date=appointment_date,
                                   appointment_time=appointment_time, appointment_description=appointment_description, user_id=user_id)
        appointment.save()
        return redirect("myappointments")
    if not request.user.is_authenticated:
        return redirect("login")
    if (request.user.username) == "doctor":
        return redirect("home")
    return render(request, "home/appoint.html")


def myappointments(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id1 = int(request.POST["app_id"])
            Appointments.objects.get(id=id1).delete()
            redirect("myappointments")
        apps = Appointments.objects.filter(user_id=request.user.id,)
        return render(request, "home/urappoint.html", {'apps': apps})
    return redirect("login")


# def doctorlogin(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         if username == "doctor" and password == "doctor123":
#             return redirect("doctor")
#             f = 1
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return render(request, 'home/doctorlogin.html')
#     return render(request, 'home/doctorlogin.html')


def doctor(request):
    if (request.user.username) == "doctor":
        if request.method == "POST":
            stat = request.POST["stat"]
            id1 = request.POST["id1"]
            sapp = Appointments.objects.get(id=id1)
            sapp.status = int(stat)
            sapp.save()

        apps = Appointments.objects.filter(status=0)

        return render(request, "home/doctor.html", {"apps": apps, })
    return redirect("home")
