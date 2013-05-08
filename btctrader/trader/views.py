from django.shortcuts import render_to_response
import markets
import forms
from models import Market


def index(request):
    markets = Market.objects.all()

    return render_to_response('trader/index.html', {'markets': markets})


def market_view(request, market_id):
    market = Market.objects.get(id=market_id)
    new_order_form = forms.NewOrderForm()

    market_api = market.market_api()

    success, err, market_price = market_api.api_get_current_market_price()

    return render_to_response('trader/market_view.html', {'market': market, 'new_order_form': new_order_form, 'market_price': market_price})