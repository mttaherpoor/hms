from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from .models import Patient,Notification
from base.models import Appointment, Billing, LabTest, MedicalRecord, Prescription


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'patient/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Patient.objects.get(user=self.request.user)

        context["patient"] = patient  
        context["notifications"] = Notification.objects.filter(patient=patient,seen=False)   
        context["appointments"] =Appointment.objects.filter(patient=patient).exclude(status__isnull=True).exclude(status="") 
        context["total_spent"] = Billing.objects.filter(patient=patient).aggregate(total_spent=Sum("total"))["total_spent"]

        return context


class AppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "patient/appointments.html"
    context_object_name = "appointments"

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return Appointment.objects.filter(patient=patient).exclude(status__isnull=True).exclude(status="")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.objects.get(user=self.request.user)
        return context
    

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    slug_field = "appointment_id"
    slug_url_kwarg = "appointment_id"
    template_name = 'patient/appointment_detail.html'

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return Appointment.objects.filter(patient=patient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Patient.objects.get(user=self.request.user)
        appointment = self.object     
    
        context["patient"] = patient  
        context["appointments"] =appointment   
        context["medical_records"] =MedicalRecord.objects.filter(appointment=appointment)
        context["lab_tests"] =LabTest.objects.filter(appointment=appointment)
        context["prescriptions"] =Prescription.objects.filter(appointment=appointment)
        
        return context


class AppointmentCancelView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],patient=patient)

        appointment.status = Appointment.APPOINTMENT_STATUS_CANCELLED
        appointment.save(update_fields=["status"])

        messages.success(request, "Appointment Cancelled Successfully")

        return redirect(appointment.get_absolute_url("patient"))


class AppointmentActivateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],patient=patient)

        appointment.status = Appointment.APPOINTMENT_STATUS_SCHEDULED
        appointment.save(update_fields=["status"])

        messages.success(request, "Appointment Re-SCHEDULED Successfully")

        return redirect(appointment.get_absolute_url("patient"))


class AppointmentCompletedView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],patient=patient)

        appointment.status = Appointment.APPOINTMENT_STATUS_COMPLETED
        appointment.save(update_fields=["status"])

        messages.success(request, "Appointment COMPLETED Successfully")

        return redirect(appointment.get_absolute_url("patient"))
