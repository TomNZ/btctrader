from django.db import models
import markets
import traders
from django.utils import timezone


class Currency(models.Model):

    name = models.CharField(max_length=256)
    abbrev = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s (%s)' % (self.abbrev, self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.abbrev = self.abbrev.upper()
        super(Currency, self).save(force_insert, force_update, using, update_fields)


class Market(models.Model):

    name = models.CharField(max_length=256)
    abbrev = models.CharField(max_length=10)
    api_name = models.CharField(max_length=256)
    default_currency_from = models.ForeignKey(Currency, related_name='default_currency_from_market_set')
    default_currency_to = models.ForeignKey(Currency, related_name='default_currency_to_market_set')
    automated_trading_enabled = models.BooleanField(blank=False, null=False, default=False)
    reserved_amount = models.DecimalField(decimal_places=5, max_digits=18, default=0)
    reserved_currency = models.ForeignKey(Currency, related_name='reserved_currency_market_set')

    # Stores persistent API objects
    apis = {}

    def __unicode__(self):
        return self.name

    @property
    def market_api(self):
        if self.id in Market.apis.keys():
            return Market.apis[self.id]
        else:
            api = markets.AVAILABLE_MARKETS[self.api_name](self)
            Market.apis[self.id] = api
            return api

    @property
    def supported_from_currencies(self):
        api = self.market_api()
        return Currency.objects.filter(abbrev__in=[pair[0] for pair in api.supported_currency_pairs])

    @property
    def supported_to_currencies(self):
        api = self.market_api()
        return Currency.objects.filter(abbrev__in=[pair[1] for pair in api.supported_currency_pairs])

    @property
    def last_market_price(self):
        api = self.market_api
        success, err, price = api.api_get_current_market_price()
        if success:
            return price
        else:
            return None


class MarketPeriod(models.Model):

    market = models.ForeignKey(Market)
    start_time = models.DateTimeField()
    period = models.IntegerField()
    open_price = models.DecimalField(decimal_places=5, max_digits=18)
    close_price = models.DecimalField(decimal_places=5, max_digits=18)
    high = models.DecimalField(decimal_places=5, max_digits=18)
    low = models.DecimalField(decimal_places=5, max_digits=18)
    volume = models.DecimalField(decimal_places=3, max_digits=16)


class Trader(models.Model):

    name = models.CharField(max_length=256)
    abbrev = models.CharField(max_length=20)
    algo_name = models.CharField(max_length=256)
    enabled = models.BooleanField(blank=False, null=False, default=True)

    # Stores persistent trading algorithm objects
    algos = {}

    def __unicode__(self):
        return self.name

    @property
    def algo(self):
        if self.id in Trader.algos.keys():
            return Trader.algos[self.id]
        else:
            algo = traders.AVAILABLE_TRADERS[self.algo_name](self)
            Trader.algos[self.id] = algo
            return algo


ORDER_TYPE_CHOICES = (
    ('B', 'Buy'),
    ('S', 'Sell'),
)

ORDER_STATUS_CHOICES = (
    ('N', 'Not submitted'),
    ('O', 'Open'),
    ('E', 'Executing'),
    ('F', 'Filled'),
    ('C', 'Cancelled'),
    ('I', 'Invalid'),
    ('U', 'Unknown'),
)


class Order(models.Model):

    order_type = models.CharField(max_length=1, choices=ORDER_TYPE_CHOICES)
    when_created = models.DateTimeField(default=timezone.now, blank=True)
    when_submitted = models.DateTimeField(blank=True, null=True)
    when_filled = models.DateTimeField(blank=True, null=True)
    when_cancelled = models.DateTimeField(blank=True, null=True)
    status = models.CharField(default='N', max_length=1, choices=ORDER_STATUS_CHOICES)
    market = models.ForeignKey(Market)
    market_order = models.BooleanField()
    amount = models.DecimalField(decimal_places=5, max_digits=18)
    currency_from = models.ForeignKey(Currency, related_name='currency_from_order_set')
    currency_to = models.ForeignKey(Currency, related_name='currency_to_order_set')
    price = models.DecimalField(blank=True, null=True, decimal_places=5, max_digits=18)
    market_order_id = models.CharField(max_length=255)
    trader = models.ForeignKey(Trader, blank=True, null=True)

    def __unicode__(self):
        return self.market_order_id

    def get_currency_pair(self, separator=''):
        return self.currency_from.abbrev + separator + self.currency_to.abbrev

    @property
    def total(self):
        return self.amount * self.price


class MarketPrice(models.Model):

    market = models.ForeignKey(Market)
    currency_from = models.ForeignKey(Currency, related_name='currency_from_marketprice_set')
    currency_to = models.ForeignKey(Currency, related_name='currency_to_marketprice_set')
    time = models.DateTimeField(default=timezone.now, blank=True)
    buy_price = models.DecimalField(decimal_places=5, max_digits=18)
    sell_price = models.DecimalField(decimal_places=5, max_digits=18)


class HistoricalTrade(models.Model):

    market = models.ForeignKey(Market)
    currency_from = models.ForeignKey(Currency, related_name='currency_from_historicaltrade_set')
    currency_to = models.ForeignKey(Currency, related_name='currency_to_historicaltrade_set')
    time = models.DateTimeField()
    amount = models.DecimalField(decimal_places=5, max_digits=18)
    price = models.DecimalField(decimal_places=5, max_digits=18)
