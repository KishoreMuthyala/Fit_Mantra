from django.db import reset_queries
from .models import Appointments, Feedbacks
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import login as kishore, authenticate, logout

import html
chatList = []


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
    if request.method == "POST":
        if "chat-user" in request.POST.keys():
            chat = request.POST["chat-user"]
            if chat != "":
                chatList.append(chat)
                if chat.lower() == "hi":
                    chatList.append("Hello! How can i help you?")
                elif chat.lower() == "how to book my appointment":
                    chatList.append(
                        "Go to book your appointment from navigation menu")
                else:
                    chatList.append("Sorry! I didn't get it")

        else:
            id1 = int(request.POST["app_id"])
            Appointments.objects.get(id=id1).delete()
            redirect("home")
    apps = Appointments.objects.filter(status=1)
    return render(request, "home/index.html", {'apps': apps, 'chats': chatList})


def appointment(request):
    if request.method == "POST":
        appo = Appointments.objects.filter(user_id=request.POST["user_id"])
        if len(appo) > 0:
            messages.error(request, "Appointment Already Taken")
        else:
            appointment_time = request.POST["app_time"]
            appointment_date = request.POST["app_date"]
            appointment_description = request.POST["app_des"]
            phone_number = request.POST["app_ph"]
            #phone_number = request.POST["phone_number"]
            user_id = request.POST["user_id"]
            appointment = Appointments(appointment_date=appointment_date,
                                       appointment_time=appointment_time, appointment_description=appointment_description, phone_number=phone_number, user_id=user_id)
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
        app = Appointments.objects.filter(user_id=request.user.id,)
        return render(request, "home/urappoint.html", {'app': app})
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


def edit(request):
    app = {}

    if request.method == "POST":
        if "user1_id" in request.POST.keys():
            id1 = request.POST.get("user1_id", 1)
            app = Appointments.objects.get(user_id=id1)
        else:
            id1 = request.POST.get("user_id1", 1)
            app = Appointments.objects.get(user_id=id1)
            app.appointment_time = request.POST["app_time"]
            app.appointment_date = request.POST["app_date"]
            app.appointment_description = request.POST["app_des"]
            app.phone_number = request.POST["app_ph"]
            #phone_number = request.POST["phone_number"]
            app.save()
            return redirect("myappointments")

    return render(request, "home/edit.html", {"app": app})


def about(request):
    return render(request, "home/about.html")


def feedback(request):
    feed_user = Feedbacks.objects.filter(user_id=request.user.id)
    allfeeds = Feedbacks.objects.all()
    if request.method == "POST":
        rate = request.POST["rate"]
        des = request.POST["suggest"]
        user_id = request.POST["user_id"]
        feed = Feedbacks(rate=rate, description=des, user_id=user_id)
        feed.save()

    return render(request, "home/feedback.html", {"feeds": feed_user, "allfeeds": allfeeds})
