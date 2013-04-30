from django.db import models

class Currency(models.Model):

    name = models.CharField(max_length=256)
    abbrev = models.CharField(max_length=10)


class Market(models.Model):

    name = models.CharField(max_length=256)
    abbrev = models.CharField(max_length=10)
    default_trade_currency = models.ForeignKey(Currency)


class MarketPeriod(models.Model):

    market = models.ForeignKey(Market)
    start_time = models.DateTimeField()
    period = models.IntegerField()
    open_price = models.DecimalField(decimal_places=5, max_digits=18)
    close_price = models.DecimalField(decimal_places=5, max_digits=18)
    high = models.DecimalField(decimal_places=5, max_digits=18)
    low = models.DecimalField(decimal_places=5, max_digits=18)
    volume = models.DecimalField(decimal_places=3, max_digits=16)


ORDER_TYPE_CHOICES = (
    ('B', 'Buy'),
    ('S', 'Sell'),
)

ORDER_STATUS_CHOICES = (
    ('O', 'Open'),
    ('F', 'Filled'),
    ('C', 'Cancelled'),
    ('U', 'Unknown'),
)

class Order(models.Model):

    order_type = models.CharField(max_length=1, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(default='U', max_length=1, choices=ORDER_STATUS_CHOICES)
    market = models.ForeignKey(Market)
    market_order = models.BooleanField()
    amount = models.DecimalField(decimal_places=5, max_digits=18)
    currency = models.ForeignKey(Currency)
    price = models.DecimalField(blank=True, null=True, decimal_places=5, max_digits=18)
    market_order_id = models.CharField(max_length=255)


class MarketPrice(models.Model):

    market = models.ForeignKey(Market)
    currency_from = models.ForeignKey(Currency, related_name='currency_from_set')
    currency_to = models.ForeignKey(Currency, related_name='currency_to_set')
    buy_price = models.DecimalField(decimal_places=5, max_digits=18)
    sell_price = models.DecimalField(decimal_places=5, max_digits=18)