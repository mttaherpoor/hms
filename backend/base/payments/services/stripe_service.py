# services/stripe_service.py

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    @staticmethod
    def create_checkout_session(*, billing, success_url, cancel_url):
        return stripe.checkout.Session.create(
            customer_email=billing.patient.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                            'name': billing.patient.full_name,
                        },
                        'unit_amount': int(billing.total * 100),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

    @staticmethod
    def retrieve_session(session_id):
        return stripe.checkout.Session.retrieve(session_id)
    