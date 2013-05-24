# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trader'
        db.create_table(u'trader_trader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('algo_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'trader', ['Trader'])

        # Adding field 'Market.automated_trading_enabled'
        db.add_column(u'trader_market', 'automated_trading_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Market.reserved_amount'
        db.add_column(u'trader_market', 'reserved_amount',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=18, decimal_places=5),
                      keep_default=False)

        # Adding field 'Market.reserved_currency'
        db.add_column(u'trader_market', 'reserved_currency',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='reserved_currency_market_set', to=orm['trader.Currency']),
                      keep_default=False)

        # Adding field 'Order.trader'
        db.add_column(u'trader_order', 'trader',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trader.Trader'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Trader'
        db.delete_table(u'trader_trader')

        # Deleting field 'Market.automated_trading_enabled'
        db.delete_column(u'trader_market', 'automated_trading_enabled')

        # Deleting field 'Market.reserved_amount'
        db.delete_column(u'trader_market', 'reserved_amount')

        # Deleting field 'Market.reserved_currency'
        db.delete_column(u'trader_market', 'reserved_currency_id')

        # Deleting field 'Order.trader'
        db.delete_column(u'trader_order', 'trader_id')


    models = {
        u'trader.currency': {
            'Meta': {'object_name': 'Currency'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'trader.market': {
            'Meta': {'object_name': 'Market'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'api_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'automated_trading_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_currency_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_currency_from_market_set'", 'to': u"orm['trader.Currency']"}),
            'default_currency_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_currency_to_market_set'", 'to': u"orm['trader.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'reserved_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '18', 'decimal_places': '5'}),
            'reserved_currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reserved_currency_market_set'", 'to': u"orm['trader.Currency']"})
        },
        u'trader.marketperiod': {
            'Meta': {'object_name': 'MarketPeriod'},
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            'high': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trader.Market']"}),
            'open_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            'period': ('django.db.models.fields.IntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '3'})
        },
        u'trader.marketprice': {
            'Meta': {'object_name': 'MarketPrice'},
            'buy_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            'currency_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currency_from_marketprice_set'", 'to': u"orm['trader.Currency']"}),
            'currency_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currency_to_marketprice_set'", 'to': u"orm['trader.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trader.Market']"}),
            'sell_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'trader.order': {
            'Meta': {'object_name': 'Order'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'}),
            'currency_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currency_from_order_set'", 'to': u"orm['trader.Currency']"}),
            'currency_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currency_to_order_set'", 'to': u"orm['trader.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trader.Market']"}),
            'market_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'market_order_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '5', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'trader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trader.Trader']", 'null': 'True', 'blank': 'True'}),
            'when_cancelled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'when_filled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'when_submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'trader.trader': {
            'Meta': {'object_name': 'Trader'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'algo_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['trader']