from django.views.generic import ListView, DetailView

from base.models import Service
from doctor.models import Doctor

class HomePageView(ListView):
    queryset = Service.objects.all()
    context_object_name = 'services'
    template_name = 'base/home.html'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'base/service_detail.html'
    
    def get_queryset(self):
        return Service.objects.prefetch_related('available_doctors')
