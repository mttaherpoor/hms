from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from base.models import Billing
from ..services.stripe_service import StripeService
from ..services.payment_service import PaymentService

@method_decorator(csrf_exempt, name='dispatch')
class StripePaymentView(View):
    def post(self, request:HttpRequest, billing_id):
        billing = get_object_or_404(Billing, billing_id=billing_id)

        success_url = request.build_absolute_uri(
            reverse("base:stripe-payment-verify", args=[billing.billing_id])
        ) + "?session_id={CHECKOUT_SESSION_ID}"

        cancel_url = request.build_absolute_uri(
            reverse("base:stripe-payment-verify", args=[billing.billing_id])
        ) + "?session_id={CHECKOUT_SESSION_ID}"

        session = StripeService.create_checkout_session(
            request=request,
            billing=billing,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return JsonResponse({"sessionId": session.id})
    

class StripePaymentVerifyView(View):
    def get(self, request:HttpRequest, billing_id):
        billing = get_object_or_404(Billing, billing_id=billing_id)
        session_id = request.GET.get("session_id")

        if not session_id:
            return redirect(self._failed_url(billing))

        session = StripeService.retrieve_session(session_id)

        if session.payment_status == "paid":
            PaymentService.mark_as_paid(billing)
            return redirect(self._success_url(billing))

        return redirect(self._failed_url(billing))

    def _success_url(self, billing):
        return f"/payment_status/{billing.billing_id}/?payment_status=paid"

    def _failed_url(self, billing):
        return f"/payment_status/{billing.billing_id}/?payment_status=failed"
