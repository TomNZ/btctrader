import base64
import hashlib
import hmac
import time
import urllib
import requests
from models import *


# Note that all public API functions are expected to return up to 3 outputs:
#   success - A True/False value indicating whether the function succeeded
#   err - If success=False, this field should be populated with an error message
#   result - If success-True, this field should be populated with the actual result of the function
# This is to avoid messy/expensive exception handling and call stack unwinds
# Please ALWAYS verify the value of success when calling an api function
# For convention, all functions implementing this return interface are prefixed with api_
class MarketBase:
    """
    Defines the interface for a Market API
    """

    # Not all markets support all currencies, and combinations thereof
    # You should define which currency pairings your market supports
    supported_currency_pairs = (
        ('BTC', 'USD'),
    )

    def api_execute_order(self, order):
        """
        Attempt to execute the specified order
        @type order: models.Order
        """
        pass

    def api_update_order_status(self, order):
        """
        Update the order object with the latest status from the market
        @type order: models.Order
        """
        pass

    def api_get_total_amount_after_fees(self, amount, order_type, currency):
        """
        Calculate the final amount, after fees have been subtracted
        Based on both a currency, and an order type (Buy/Sell)
        @type currency: models.Currency
        """
        pass

    def api_get_total_amount_incl_fees(self, amount, order_type, currency):
        """
        Calculate a total amount required for a trade, such that the target
        amount is a certain value, once fees have been subtracted (i.e. this
        gives the total amount INCLUDING fees)
        Based on both a currency, and an order type (Buy/Sell)
        @type currency: models.Currency
        """
        pass


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

    supported_currency_pairs = (
        ('BTC', 'USD'),
        ('BTC', 'GBP'),
        ('BTC', 'EUR'),
        ('BTC', 'JPY'),
        ('BTC', 'AUD'),
        ('BTC', 'CAD'),
        ('BTC', 'CHF'),
        ('BTC', 'CNY'),
        ('BTC', 'DKK'),
        ('BTC', 'HKD'),
        ('BTC', 'PLN'),
        ('BTC', 'RUB'),
        ('BTC', 'SEK'),
        ('BTC', 'SGD'),
        ('BTC', 'THB'),
    )

    timeout = 15
    tryout = 5

    def __init__(self):
        # Change these to reflect your actual API keys
        self.api_key = '86c19e46-6e8e-4093-b876-4ca116170658'
        self.api_secret = 'WOKFhfhlRxifCo5cogriTddCBrZ0RNar7VH4K/xioXr/oo77oaBy9lX7OC62oHJbRPQU1GTc0JRAAcKFov6lOw=='

        self.trade_fee = 0
        self.trade_fee_valid = False

        self.time = {'init': time.time(), 'req': time.time()}
        self.reqs = {'max': 10, 'window': 10, 'curr': 0}

        self.default_currency_pair = 'BTCUSD'

    def throttle(self):
        # check that in a given time window (10 seconds),
        # no more than a maximum number of requests (10)
        # have been sent, otherwise sleep for a bit
        diff = time.time() - self.time['req']
        if diff > self.reqs['window']:
            self.reqs['curr'] = 0
            self.time['req'] = time.time()
        self.reqs['curr'] += 1
        if self.reqs['curr'] > self.reqs['max']:
            print 'Request limit reached...'
            time.sleep(self.reqs['window'] - diff)

    def nonce(self):
        return str(int(time.time() * 1000))

    def api_request(self, path, post_data=None):
        if post_data is None:
            post_data = []

        # Add the nonce
        post_data.insert(0, ('nonce', self.nonce()))

        # Build the POST data
        post_data_str = urllib.urlencode(post_data)

        # Build the encryption
        hash_data = path + chr(0) + post_data_str
        signature = base64.b64encode(str(hmac.new(
            base64.b64decode(self.api_secret),
            hash_data,
            hashlib.sha512
        ).digest()))

        # Build the headers
        headers = {
            'User-Agent': 'btctrader',
            'Rest-Key': self.api_key,
            'Rest-Sign': signature,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        tries = 0
        resp = None
        while tries < self.tryout:
            tries += 1

            # We want a hard throttle on requests to avoid being blocked
            self.throttle()

            # Make the actual request
            try:
                resp = requests.post(MTGOX_API_BASE_URL + path,
                                     data=post_data_str,
                                     headers=headers,
                                     timeout=self.timeout)
            except requests.Timeout:
                continue

            # If we got to here, the request did not timeout
            break

        # Check for failure response
        if resp is None or resp.status_code != 200:
            return False, 'HTTP request failed: API returned status %s (request path %s)' % resp.status_code, path

        resp_json = resp.json()
        if resp_json['result'] != 'success':
            return False, 'API request did not return success response (request path %s)' % path
        else:
            return True, None, resp_json['data']

    def api_get_info(self):
        return self.api_request(self.default_currency_pair + '/money/info')

    def api_get_trade_fee(self):
        if not self.trade_fee_valid:
            success, err, info = self.api_get_info()
            if not success:
                return success, err

            self.trade_fee = float(info['Trade_Fee'])
            self.trade_fee_valid = True

        return True, None, self.trade_fee

    def get_order_currency_pair(self, order):
        return order.currency_from.abbrev.upper() + order.currency_to.abbrev.upper()

    def api_execute_order(self, order):
        # Should we even be executing this order?
        if order.amount < MTGOX_MINIMUM_TRADE_BTC:
            return False, 'Trade amount lower than MtGox minimum trade'
        if order.status != 'N':
            return False, 'Order has already been submitted to MtGox'
        if not (order.currency_from.abbrev.upper(), order.currency_to.abbrev.upper()) in self.supported_currency_pairs:
            return False, 'MtGox does not support this currency pairing'

        # Get the current trade fee associated with this account
        success, err, fee = self.api_get_trade_fee()
        if not success:
            return success, err

        # Build the trade request

        # Account for the trade fee

        # Send the trade request

        # Invalidate trade fee
        self.trade_fee_valid = False

    def api_update_order_status(self, order):
        # Currently the v2 API call for info on a specific order is broke
        # Hence retrieve info for all orders and filter from there
        success, err, result = self.api_request(self.get_order_currency_pair(order) + '/money/orders')
        if not success:
            return success, err

        found = False
        for open_order in result:
            if open_order['oid'] == order.market_order_id:
                # Validate order parameters - if MtGox doesn't agree with the database then there's a serious problem
                if open_order['currency'] != order.currency_to.abbrev.upper():
                    return False, 'Order currency_to does not match expected value (expected %s, got %s)' %\
                                  order.currency_to.abbrev.upper(), open_order['currency']
                if open_order['item'] != order.currency_from.abbrev.upper():
                    return False, 'Order currency_from does not match expected value (expected %s, got %s)' %\
                                  order.currency_from.abbrev.upper(), open_order['item']
                if open_order['amount'] != order.amount:
                    return False, 'Order amount does not match expected value (expected %s, got %s)' %\
                                  order.amount, open_order['amount']
                if order.market_order and float(open_order['price']) != 0:
                    return False, 'Order expected to be a market order, got price %s' % open_order['price']

                # Update status
                if open_order['status'] in ['pending', 'executing', 'post-pending']:
                    order.status = 'E'
                elif open_order['status'] == 'open':
                    order.status = 'O'
                elif open_order['status'] == 'invalid':
                    order.status = 'I'
                else:
                    order.status = 'U'

                found = True
                break

        if not found:
            # /money/orders does not return filled orders - if it wasn't found, assume it was filled
            # TODO: Could it have been cancelled?
            order.status = 'F'

        order.save()

        return True, None