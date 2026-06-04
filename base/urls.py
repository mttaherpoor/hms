from django.urls import path

from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('service/<int:pk>/',views.ServiceDetailView.as_view(),name='service_detail'),
    path('service/<int:service_id>/book/<int:doctor_id>/',views.BookAppointmentView.as_view(),name='book_appointment'),

]
