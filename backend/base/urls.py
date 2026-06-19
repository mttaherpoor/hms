from django.urls import path

from . import views
from .payments.views import stripe
from .payments.views import paypal

app_name = 'base'

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('service/<int:pk>/',views.ServiceDetailView.as_view(),name='service-detail'),
    path('service/<int:service_id>/book/<int:doctor_id>/',views.BookAppointmentView.as_view(),name='book-appointment'),
    path('checkout/<str:billing_id>/',views.CheckoutView.as_view(),name='checkout'),
    path('payment/<str:billing_id>/status/',views.PaymentStatusView.as_view(),name='payment-status'),
   
    # stripe
    path('payments/stripe/<str:billing_id>/create/', stripe.StripePaymentView.as_view(), name='stripe-payment'),
    path('payments/stripe/<str:billing_id>/verify/', stripe.StripePaymentVerifyView.as_view(), name='stripe-payment-verify'),

    # paypal
    path('payments/paypal/<str:billing_id>/verify/', paypal.PayPalPaymentVerifyView.as_view(), name='paypal-payment-verify'),
]
