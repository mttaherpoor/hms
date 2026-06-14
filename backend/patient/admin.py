from django.contrib import admin

from .models import Patient, Notification


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'mobile', 'gender', 'dob']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type', 'seen', 'datetime_created']