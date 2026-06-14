from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView, ListView, View

from .models import Doctor,Notification
from base.models import Appointment, LabTest, MedicalRecord, Prescription

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(user=self.request.user)

        context["doctor"] = doctor  
        context["notifications"] = Notification.objects.filter(doctor=doctor)   
        context["appointments"] =Appointment.objects.filter(doctor=doctor) 
        
        return context
    

class AppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "doctor/appointments.html"
    context_object_name = "appointments"

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Appointment.objects.filter(doctor=doctor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.get(user=self.request.user)
        return context
    

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    slug_field = "appointment_id"
    slug_url_kwarg = "appointment_id"
    template_name = 'doctor/appointment_detail.html'

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Appointment.objects.filter(doctor=doctor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(user=self.request.user)
        appointment = self.object     
    
        context["doctor"] = doctor  
        context["appointments"] =appointment   
        context["medical_recoreds"] =MedicalRecord.objects.filter(appointment=appointment)
        context["lab_tests"] =LabTest.objects.filter(appointment=appointment)
        context["prescriptions"] =Prescription.objects.filter(appointment=appointment)
        
        return context


class AppointmentCancelView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        doctor = Doctor.objects.get(user=request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],doctor=doctor)

        appointment.status = Appointment.APPOINTMENT_STATUS_CANCELLED
        appointment.save(update_fields=["status"])

        messages.success(request, "Appointment Cancelled Successfully")

        return redirect(appointment.get_absolute_url())


class AppointmentActivateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        doctor = Doctor.objects.get(user=request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],doctor=doctor)

        appointment.status = Appointment.APPOINTMENT_STATUS_SCHEDULED
        appointment.save(update_fields=["status"])

        messages.success(request, "Appointment Re-SCHEDULED Successfully")

        return redirect(appointment.get_absolute_url())


class AppointmentCompletedView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        doctor = Doctor.objects.get(user=request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],doctor=doctor)

        appointment.status = Appointment.APPOINTMENT_STATUS_COMPLETED
        appointment.save(update_fields=["status"])

        messages.success(request, "Appointment COMPLETED Successfully")

        return redirect(appointment.get_absolute_url())
