from django.urls import path

from . import views

app_name = 'doctor'

urlpatterns = [
    path('',views.DashboardView.as_view(),name='dashboard'),
    path('appointments/',views.AppointmentsView.as_view(),name='appointment-list'),
    path('appointments/<str:appointment_id>/',views.AppointmentDetailView.as_view(),name='appointment-detail'),

    path('appointments/<str:appointment_id>/cancel/',views.AppointmentCancelView.as_view(),name='appointment-cancel'),
    path('appointments/<str:appointment_id>/aactivate/',views.AppointmentActivateView.as_view(),name='appointment-activate'),
    path('appointments/<str:appointment_id>/acomplete/',views.AppointmentCompletedView.as_view(),name='appointment-completed'),


]