from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from decimal import Decimal

from .models import Service, Appointment, Billing
from .forms import AppointmentBookingForm
from doctor.models import Doctor
from patient.models import Patient
from patient.forms import PatientForm

TAX_RATE = Decimal(0.05)

class HomePageView(ListView):
    queryset = Service.objects.all()
    context_object_name = 'services'
    template_name = 'base/home.html'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'base/service_detail.html'
    
    def get_queryset(self):
        return Service.objects.prefetch_related('available_doctors')


class BookAppointmentView(LoginRequiredMixin, FormView):
    template_name = "base/book_appointment.html"
    form_class = PatientForm

    def get_service(self):
        return get_object_or_404(
            Service,
            pk=self.kwargs["service_id"]
        )

    def get_doctor(self):
        return get_object_or_404(
            Doctor,
            pk=self.kwargs["doctor_id"]
        )

    def get_patient(self):
        return get_object_or_404(
            Patient,
            user=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_patient()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["service"] = self.get_service()
        context["doctor"] = self.get_doctor()
        context["patient"] = self.get_patient()

        return context

    def form_valid(self, form):
        service = self.get_service()
        doctor = self.get_doctor()

        patient = form.save(commit=False)
        patient.email = self.get_patient().email
        patient = form.save()

        appointment = Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=form.cleaned_data["issues"],
            symptoms=form.cleaned_data["symptoms"],
        )

        billing = Billing.objects.create(
            patient=patient,
            appointment=appointment,
            sub_total=service.cost,
            tax=service.cost * TAX_RATE,
            total=service.cost * (1 + TAX_RATE),
            status="Unpaid",
        )

        return redirect("checkout",billing.billing_id)   
