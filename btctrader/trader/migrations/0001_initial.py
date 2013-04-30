# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'trader_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'trader', ['Currency'])

        # Adding model 'Market'
        db.create_table(u'trader_market', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('default_trade_currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trader.Currency'])),
        ))
        db.send_create_signal(u'trader', ['Market'])

        # Adding model 'MarketPeriod'
        db.create_table(u'trader_marketperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trader.Market'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
            ('open_price', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
            ('close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
            ('high', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
            ('low', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=3)),
        ))
        db.send_create_signal(u'trader', ['MarketPeriod'])

        # Adding model 'Order'
        db.create_table(u'trader_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('status', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trader.Market'])),
            ('market_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
            ('currency_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='currency_from_order_set', to=orm['trader.Currency'])),
            ('currency_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='currency_to_order_set', to=orm['trader.Currency'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=5, blank=True)),
            ('market_order_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'trader', ['Order'])

        # Adding model 'MarketPrice'
        db.create_table(u'trader_marketprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trader.Market'])),
            ('currency_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='currency_from_marketprice_set', to=orm['trader.Currency'])),
            ('currency_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='currency_to_marketprice_set', to=orm['trader.Currency'])),
            ('buy_price', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
            ('sell_price', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=5)),
        ))
        db.send_create_signal(u'trader', ['MarketPrice'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table(u'trader_currency')

        # Deleting model 'Market'
        db.delete_table(u'trader_market')

        # Deleting model 'MarketPeriod'
        db.delete_table(u'trader_marketperiod')

        # Deleting model 'Order'
        db.delete_table(u'trader_order')

        # Deleting model 'MarketPrice'
        db.delete_table(u'trader_marketprice')


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
            'default_trade_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trader.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
            'sell_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '5'})
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
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        }
    }

    complete_apps = ['trader']