from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView, View, CreateView, UpdateView

from .forms import DoctorForm
from .models import Doctor,Notification
from base.models import Appointment, Billing, LabTest, MedicalRecord, Prescription

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(user=self.request.user)

        context["doctor"] = doctor  
        context["notifications"] = Notification.objects.filter(doctor=doctor,seen=False)   
        context["appointments"] =Appointment.objects.filter(doctor=doctor).exclude(status__isnull=True).exclude(status="") 
        
        return context
    

class AppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "doctor/appointments.html"
    context_object_name = "appointments"

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Appointment.objects.filter(doctor=doctor).exclude(status__isnull=True).exclude(status="")

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
        context["medical_records"] =MedicalRecord.objects.filter(appointment=appointment)
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


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    fields = ["diagnosis", "treatment"]

    def form_valid(self, form):
        doctor = Doctor.objects.get(user=self.request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],doctor=doctor)

        form.instance.appointment = appointment

        messages.success(self.request, "Medical Record Added Successfully")

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.appointment.get_absolute_url()
    

class MedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    fields = ["diagnosis", "treatment"]

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return MedicalRecord.objects.filter(appointment__doctor=doctor)
        
    def form_valid(self, form):
        messages.success(self.request, "Medical Record Updated Successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.appointment.get_absolute_url()


class LabTestCreateView(LoginRequiredMixin, CreateView):
    model = LabTest
    fields = ["test_name", "description", "result"]

    def form_valid(self, form):
        doctor = Doctor.objects.get(user=self.request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],doctor=doctor)

        form.instance.appointment = appointment

        messages.success(self.request, "Lab Tests Added Successfully")

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.appointment.get_absolute_url()
    

class LabTestUpdateView(LoginRequiredMixin, UpdateView):
    model = LabTest
    fields = ["test_name", "description", "result"]


    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return LabTest.objects.filter(appointment__doctor=doctor)
        
    def form_valid(self, form):
        messages.success(self.request, "Lab Tests Updated Successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.appointment.get_absolute_url()


class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ["medications"]

    def form_valid(self, form):
        doctor = Doctor.objects.get(user=self.request.user)

        appointment = get_object_or_404(Appointment,appointment_id=self.kwargs["appointment_id"],doctor=doctor)

        form.instance.appointment = appointment

        messages.success(self.request, "Prescriptions Added Successfully")

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.appointment.get_absolute_url()
    

class PrescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescription
    fields = ["medications"]


    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Prescription.objects.filter(appointment__doctor=doctor)
        
    def form_valid(self, form):
        messages.success(self.request, "Prescriptions Updated Successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.appointment.get_absolute_url()


class PaymentView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = 'doctor/payments.html'
    context_object_name = 'payments'

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)

        return Billing.objects.select_related(
            'patient',
            'appointment',
            'appointment__service',
        ).filter(
            appointment__doctor=doctor,
            status=Billing.BILLING_STATUS_PAID
        )


class NotificationView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "doctor/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)

        return Notification.objects.select_related(
            "appointment",
            "appointment__patient",
        ).filter(
            doctor=doctor,
            seen=False,
        )
    

class NotificationSeenView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        notification = get_object_or_404(
            Notification,
            pk=self.kwargs["pk"],
            doctor__user=request.user,
        )

        notification.seen = True
        notification.save(update_fields=["seen"])

        messages.success(request, "Notification marked as seen")

        return redirect("doctor:notifications")


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "doctor/profile.html"
    form_class = DoctorForm
    model = Doctor
    context_object_name = 'doctor'

    def get_object(self, queryset=None):
        return Doctor.objects.get(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("doctor:profile")    
               