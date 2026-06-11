from django.urls import path

from . import views
from .payments.views import stripe

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('service/<int:pk>/',views.ServiceDetailView.as_view(),name='service_detail'),
    path('service/<int:service_id>/book/<int:doctor_id>/',views.BookAppointmentView.as_view(),name='book_appointment'),
    path('checkout/<str:billing_id>/',views.CheckoutView.as_view(),name='checkout'),
    path('payment_status/<str:billing_id>/',views.PaymentStatusView.as_view(),name='payment_status'),
   
    # stripe
    path('stripe_payment/<str:billing_id>/', stripe.StripePaymentView.as_view(), name='stripe_payment'),
    path('stripe_payment_verify/<str:billing_id>/', stripe.StripePaymentVerifyView.as_view(), name='stripe_payment_verify'),
]
