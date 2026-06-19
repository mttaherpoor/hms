from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView

from decimal import Decimal

from .models import Service, Appointment, Billing
from doctor.models import Doctor
from patient.models import Patient
from patient.forms import PatientAppointmentForm

TAX_RATE = Decimal("0.05")

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
    form_class = PatientAppointmentForm

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
        patient.save()

        appointment = Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=form.cleaned_data["issues"],
            symptoms=form.cleaned_data["symptoms"],
        )

        sub_total = service.cost
        tax = (sub_total * TAX_RATE).quantize(Decimal("0.01"))
        total = (sub_total + tax).quantize(Decimal("0.01"))

        billing = Billing.objects.create(
            patient=patient,
            appointment=appointment,
            sub_total=sub_total,
            tax=tax,
            total=total,
            status=Billing.BILLING_STATUS_UNPAID,
        )   

        return redirect(billing.get_absolute_url())   


class CheckoutView(LoginRequiredMixin, DetailView):
    model = Billing
    template_name = "base/checkout.html"

    slug_field = "billing_id"
    slug_url_kwarg = "billing_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key']=settings.STRIPE_PUBLIC_KEY
        context['paypal_client_id']=settings.PAYPAL_CLIENT_ID

        return context


class PaymentStatusView(LoginRequiredMixin, TemplateView):
    template_name = "base/payment_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        billing = Billing.objects.get(
            billing_id=self.kwargs["billing_id"]
        )

        context.update({
            "billing": billing,
            "payment_status": self.request.GET.get("payment_status"),
        })

        return context
