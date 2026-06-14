from django.contrib import admin

from .models import Doctor, Notification

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialization', 'qualifications', 'years_of_experience']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'datetime_created']
