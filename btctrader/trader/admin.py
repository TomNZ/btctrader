from django.contrib import admin
from trader import models


class CurrencyAdmin(admin.ModelAdmin):
    pass


class MarketAdmin(admin.ModelAdmin):
    pass


class MarketPeriodAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


class MarketPriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Market, MarketAdmin)
admin.site.register(models.MarketPeriod, MarketPeriodAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.MarketPrice, MarketPriceAdmin)
