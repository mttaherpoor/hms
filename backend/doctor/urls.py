from django.urls import path

from . import views

app_name = 'doctor'

urlpatterns = [
    path('',views.DashboardView.as_view(),name='dashboard'),
    path('appointments/',views.AppointmentsView.as_view(),name='appointment-list'),
    path('appointments/<str:appointment_id>/',views.AppointmentDetailView.as_view(),name='appointment-detail'),

    path('appointments/<str:appointment_id>/cancel/',views.AppointmentCancelView.as_view(),name='appointment-cancel'),
    path('appointments/<str:appointment_id>/activate/',views.AppointmentActivateView.as_view(),name='appointment-activate'),
    path('appointments/<str:appointment_id>/complete/',views.AppointmentCompletedView.as_view(),name='appointment-completed'),

    path('appointments/<str:appointment_id>/medical-records/create/',views.MedicalRecordCreateView.as_view(),name='medical-record-create'),
    path('appointments/<str:appointment_id>/medical-records/<int:pk>/update/',views.MedicalRecordUpdateView.as_view(),name='medical-record-update'),

    path('appointments/<str:appointment_id>/lab-tests/create/',views.LabTestCreateView.as_view(),name='lab-test-create'),
    path('appointments/<str:appointment_id>/lab-tests/<int:pk>/update/',views.LabTestUpdateView.as_view(),name='lab-test-update'),

    path('appointments/<str:appointment_id>/prescriptions/create/',views.PrescriptionCreateView.as_view(),name='prescription-create'),
    path('appointments/<str:appointment_id>/prescriptions/<int:pk>/update/',views.PrescriptionUpdateView.as_view(),name='prescription-update'),

    path('payments/',views.PaymentView.as_view(),name='payments'),

    path('notifications/',views.NotificationView.as_view(),name='notifications'),
    path("notifications/<int:pk>/seen/",views.NotificationSeenView.as_view(),name="notification-seen"),

    path('profile/',views.ProfileView.as_view(),name='profile'),

]