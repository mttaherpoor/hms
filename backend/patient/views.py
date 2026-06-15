from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from .models import Patient,Notification
from base.models import Appointment, Billing


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
