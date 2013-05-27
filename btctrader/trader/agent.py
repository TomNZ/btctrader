from django.utils import timezone
from celery import Celery
from models import Market, Order, Trader, HistoricalTrade
from trader_settings import trader_settings
import requests
from datetime import timedelta


default_settings = trader_settings()

celery = Celery('agent', broker='django://')

MARKET_HISTORICAL_DATA_MAP = {
    'mtgox': ('mtgoxUSD', 'BTC', 'USD'),

}

BITCOINCHARTS_TRADES_URL = 'http://api.bitcoincharts.com/v1/trades.csv?symbol=%s&end=%s'


@celery.task
def import_historical_data():
    for api_name, params in MARKET_HISTORICAL_DATA_MAP:
        market = Market.objects.get(api_name=api_name)
        symbol = params[0]
        currency_from = params[1]
        currency_to = params[2]

        min_time = timezone.now() + timedelta(days=-default_settings.historical_trades_days_to_keep)

        existing_trades = HistoricalTrade.objects.filter(market=market, time__gt=min_time, time__lt=timezone.now())\
                                                 .order_by('-time')

        if len(existing_trades) > 0:
            latest_trade = existing_trades[0]

            if

        path = BITCOINCHARTS_TRADES_URL % (symbol, timestamp)
        resp = requests.get(path)



def update_prices(markets, timestamp, settings):
    for market in markets:
        # Update prices based for given time range
        pass


@celery.task
def build_orders(markets, traders, timestamp, settings):
    """
    Core logic of the trading bot. Inspects historical and current
    data and uses this to build a set of candidate orders that are
    subsequently executed. Assumes latest market data is already
    present and should not make any API calls of its own.

    This function will not use any data newer than the "timestamp"
    passed in to make its trading decisions. Therefore, it can be
    used to run historical simulations for performance optimization.

    This function is also "const" in that it will not modify or add
    anything to the database.
    """

    orders = []

    # Run various trade algorithms
    for trader in traders:
        orders.append(trader.algo.build_orders(markets, timestamp, settings))

    return orders


def execute_orders(orders):
    for order in orders:
        order.market.market_api.api_execute_order(order)


@celery.task
def run_trader(
        should_update_prices=True,
        should_execute_orders=True,
        timestamp=None,
        markets=None,
        traders=None,
        settings=None):
    """
    This is the function that should be called for real-time live
    trades. Performs full logic, including ensuring data is up to
    date, and executing the actual orders.
    """

    # Initialize parameters to sensible defaults if not passed
    if timestamp is None:
        timestamp = timezone.now()

    if markets is None:
        markets = Market.objects.filter(automated_trading_enabled=True)

    if traders is None:
        traders = Trader.objects.filter(enabled=True)

    if settings is None:
        settings = trader_settings()

    # Update prices
    if should_update_prices:
        update_prices(markets, timestamp, settings)

    # Build orders
    orders = build_orders(markets, traders, timestamp, settings)

    # Save orders - build_orders does not do this itself
    Order.objects.bulk_create(orders)

    # Execute orders
    if should_execute_orders:
        execute_orders(orders)

    return orders