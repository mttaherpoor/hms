from django.views.generic import DetailView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor,Notification
from base.models import Appointment

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(user=self.request.user)

        context["doctor"] = doctor  
        context["notifications"] = Notification.objects.filter(doctor=doctor)   
        context["appointments"] =Appointment.objects.filter(doctor=doctor) 
        
        return context
    
