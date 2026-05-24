from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from base import models


class AppointmentInline(admin.TabularInline):
    model = models.Appointment
    extra = 1


class MedicalRecordInline(admin.TabularInline):
    model = models.MedicalRecord
    extra = 1


class LabTestInline(admin.TabularInline):
    model = models.LabTest
    extra = 1


class PrescriptionInline(admin.TabularInline):
    model = models.Prescription
    extra = 1


class BillingInline(admin.TabularInline):
    model = models.Billing
    extra = 1

@admin.register(models.Service)
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ['name', 'cost']
    search_fields = ['name', 'description']
    filter_horizontal = ['available_doctors']

@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status']
    search_fields = ['patient__username', 'doctor__user__username']
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline, BillingInline]


@admin.register(models.MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis']


@admin.register(models.LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'test_name']


@admin.register(models.Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'medications']


@admin.register(models.Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'total', 'status', 'date']

