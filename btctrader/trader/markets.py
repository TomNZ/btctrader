import base64
import gzip
import hashlib
import hmac
import json
import time
import urllib
import requests
from models import *


# Defines the interface for a Market API
class MarketBase:

    def execute_order(self, order):
        pass

    def update_order_status(self, order):
        pass


# Change these to reflect your actual API keys
MTGOX_API_KEY = '86c19e46-6e8e-4093-b876-4ca116170658'
MTGOX_API_SECRET = 'WOKFhfhlRxifCo5cogriTddCBrZ0RNar7VH4K/xioXr/oo77oaBy9lX7OC62oHJbRPQU1GTc0JRAAcKFov6lOw=='

# Be VERY careful - should NOT be changed unless no longer correct
MTGOX_CURRENCY_DIVISIONS = (
    ('BTC', 100000000),
    ('USD', 100000),
    ('GBP', 100000),
    ('EUR', 100000),
    ('JPY', 1000),
    ('AUD', 100000),
    ('CAD', 100000),
    ('CHF', 100000),
    ('CNY', 100000),
    ('DKK', 100000),
    ('HKD', 100000),
    ('PLN', 100000),
    ('RUB', 100000),
    ('SEK', 1000),
    ('SGD', 100000),
    ('THB', 100000),
)

# Constant value enforced in the API
MTGOX_MINIMUM_TRADE_BTC = 0.01

MTGOX_API_BASE_URL = 'https://data.mtgox.com/api/2/'

class MtGoxMarket(MarketBase):

    trade_fee = 0
    trade_fee_valid = False


    def nonce(self):
        return str(int(time.time() * 1000))

    def api_request(self, path, post_data=None):
        if post_data is None:
            post_data = []

        # Add the nonce
        post_data.insert(0, ('nonce', self.nonce()))

        post_data_str = urllib.urlencode(post_data)

        # Build the encryption
        hash_data = path + chr(0) + post_data_str
        secret = base64.b64decode(MTGOX_API_SECRET)
        signature = base64.b64encode(str(hmac.new(secret, hash_data, hashlib.sha512).digest()))

        headers = {
            'User-Agent': 'btctrader',
            'Rest-Key': MTGOX_API_KEY,
            'Rest-Sign': signature,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        resp = requests.post(MTGOX_API_BASE_URL + path, data=post_data_str, headers=headers)

        # Check for 200
        if resp.status_code != 200:
            return False

        return resp.json()


    def get_info(self):
        return self.api_request('BTCUSD/money/info')


    def get_trade_fee(self):
        info = self.get_info()

        if not info:
            return False

        return float(info['data']['Trade_Fee'])


    def execute_order(self, order):
        # Is the order amount sufficient?
        if order.amount < MTGOX_MINIMUM_TRADE_BTC:
            return False

        fee = self.get_trade_fee()


    def update_order_status(self, order):
        pass