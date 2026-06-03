from django.views.generic import ListView, DetailView

from base.models import Service

class HomePageView(ListView):
    queryset = Service.objects.all()
    context_object_name = 'services'
    template_name = 'home.html'


class ServiceDetailView(DetailView):
    pass