# Generated by Django 3.0.8 on 2021-04-16 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210416_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointments',
            name='keys',
        ),
        migrations.AddField(
            model_name='appointments',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]