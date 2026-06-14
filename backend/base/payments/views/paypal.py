from django.shortcuts import get_object_or_404, redirect
from django.views import View

from django.http import HttpRequest

from base.models import Billing
from ..services.paypal_service import PayPalService
from ..services.payment_service import PaymentService


class PayPalPaymentVerifyView(View):
    def get(self, request:HttpRequest, billing_id):
        billing = get_object_or_404(Billing, billing_id=billing_id)

        order_id = request.GET.get("token")  # PayPal standard

        if not order_id:
            return redirect(self._failed_url(billing))

        try:
            order_data = PayPalService.get_order(order_id)
        except Exception:
            return redirect(self._failed_url(billing))

        if order_data.get("status") == "COMPLETED":
            PaymentService.mark_as_paid(billing)
            return redirect(self._success_url(billing))

        return redirect(self._failed_url(billing))

    def _success_url(self, billing):
        return f"/payment_status/{billing.billing_id}/?payment_status=paid"

    def _failed_url(self, billing):
        return f"/payment_status/{billing.billing_id}/?payment_status=failed"
    
