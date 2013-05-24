

class TraderBase(object):
    """
    Defines the interface for a trading algorithm
    """

    def __init__(self, trader):
        """
        Instantiate the Trader Algorithm object. Stores a pointer back to the Trader
        database object
        """
        self.trader = trader

    def build_orders(self, markets, timestamp, settings):
        """
        Build a list of orders for the given input Market list and timestamp
        """
        return []

    def get_settings_dict(self, settings):
        if self.trader.abbrev in settings.algo.keys():
            return settings.algo[self.trader.abbrev]
        else:
            return {}


class ArbitrageTrader(TraderBase):
    """
    Simple trader built on the idea of arbitrage.

    Buy on one market and sell on another to take advantage of differing exchange rates.

    Takes fees and buy/sell spread into account to ensure an overall profit. Care should
    be taken to configure the algorithm correctly in order to limit excessive trading.
    """

    def build_orders(self, markets, timestamp, trader_settings):
        settings = self.get_settings_dict(trader_settings)

        # Only run if we have more than one available market
        if len(markets) <= 1:
            return []

        orders = []

        # Run over alternate pairs of markets
        # TODO: Optimize this code block!
        for market_a in markets:
            for market_b in markets:
                if market_a.id != market_b.id:
                    pass

        return orders


class EmaTrader(TraderBase):
    """
    Trader built on the concept of EMA (Exponential Moving Average) crossover.

    Buy or sell, using EMA crossover as an indicator of a trend change.

    Ensure you configure the algorithm correctly.
    """
    def build_orders(self, markets, timestamp, trader_settings):
        settings = self.get_settings_dict(trader_settings)

        orders = []

        # Run over each market
        for market in markets:
            pass

        return orders


AVAILABLE_TRADERS = {
    'arbitrage': ArbitrageTrader,
    'ema': EmaTrader,
}