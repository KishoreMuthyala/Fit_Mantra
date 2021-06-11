from django.db import models
from django.contrib.auth.models import User


class Appointments(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    appointment_date = models.TextField()
    appointment_time = models.CharField(max_length=200)
    appointment_description = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    status = models.IntegerField(default=0)


class Feedbacks(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rate = models.IntegerField(default=0)
    description = models.TextField()
