# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Market.api_name'
        db.add_column(u'trader_market', 'api_name',
                      self.gf('django.db.models.fields.CharField')(default='mtgox', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Market.api_name'
        db.delete_column(u'trader_market', 'api_name')


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