import hashlib
import urllib

from django.conf import settings


class PayFastUtil(object):

    def __init__(self):
        """Initialising my class."""
        self.MERCHANT_ID = settings.PAYFAST_MERCHANT_ID
        self.MERCHANT_KEY = settings.PAYFAST_MERCHANT_KEY
        self.BASE_URL = settings.PAYFAST_BASE_URL

    def generate_form(self, buyer, order, amount, url=None):
        """Generate payment form."""
        data = {
            # Merchant details
            'merchant_id': self.MERCHANT_ID,
            'merchant_key': self.MERCHANT_KEY,
            'return_url': f'{url}?action=return',
            'cancel_url': f'{url}?action=cancel',
            'notify_url': f'{url}?action=notify',
            # Buyer details
            'name_first': buyer['first_name'],
            'name_last': buyer['last_name'],
            'email_address': buyer['email'],
            # Transaction details
            'm_payment_id': '1234',  # Unique payment ID to pass through to notify_url
            'amount': f"{amount}",
            'item_name': 'Order#123'
        }
        # Generate signature (see step 2)
        signature = self.generate_signature(data)
        data['signature'] = signature

        html_form = f'<form action="https://{self.BASE_URL}/eng/process" method="post">'
        for key in data:
            html_form += f'<input name="{key}" type="hidden" value="{data[key]}" />'

        html_form += '<input class="main-button" type="submit" value="Pay Now" /></form>'
        return html_form

    def generate_signature(self, data_array, pass_phrase=''):
        payload = ""
        for key in data_array:
            # Get all the data from PayFast and prepare parameter string
            payload += key + "=" + urllib.parse.quote_plus(data_array[key].replace("+", " ")) + "&"
        # After looping through, cut the last & or append your passphrase
        payload = payload[:-1]
        if pass_phrase != '':
            payload += f"&passphrase={pass_phrase}"
        return hashlib.md5(payload.encode()).hexdigest()

