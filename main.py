import requests
import hmac
import hashlib
import time
import json

class BitflyerAPI:
    def __init__(self, api_key, api_secret):
        self.base_url = "https://api.bitflyer.com/v1/"
        self.api_key = api_key
        self.api_secret = api_secret

    def get_ticker(self, product_code="BTC_JPY"):
        """
        Get ticker data.
        """
        endpoint = "ticker"
        params = {
            "product_code": product_code
        }
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json()

    def place_market_order(self, product_code, side, size):
        """
        Place a market order.
        """
        endpoint = "me/sendchildorder"
        method = "POST"
        body = {
            "product_code": product_code,
            "child_order_type": "MARKET",
            "side": side,
            "size": size
        }
        headers = self._get_private_headers(endpoint, method, body)
        response = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(body))
        return response.json()

    def _get_private_headers(self, endpoint, method, body):
        """
        Create headers for private API requests.
        """
        timestamp = str(time.time())
        text = timestamp + method + "/v1/" + endpoint + json.dumps(body)
        sign = hmac.new(bytes(self.api_secret.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

        headers = {
            'ACCESS-KEY': self.api_key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }
        return headers
