import requests
from django.conf import settings


class PayPalService:
    BASE_URL = "https://api-m.sandbox.paypal.com"

    @staticmethod
    def get_access_token():
        url = f"{PayPalService.BASE_URL}/v1/oauth2/token"

        data = {"grant_type": "client_credentials"}
        auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)

        response = requests.post(url, data=data, auth=auth)

        if response.status_code == 200:
            return response.json()["access_token"]

        raise Exception("Failed to get PayPal access token")

    @staticmethod
    def get_order(order_id):
        url = f"{PayPalService.BASE_URL}/v2/checkout/orders/{order_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PayPalService.get_access_token()}",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
    