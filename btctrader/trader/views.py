from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
import markets
import forms
from models import Market, Order


def index(request):
    markets = Market.objects.all()

    return render_to_response('trader/index.html', {'markets': markets})


def market_view(request, market_id):
    market = Market.objects.get(id=market_id)
    new_order_form = forms.NewOrderForm()

    market_api = market.market_api()

    success, err, market_price = market_api.api_get_current_market_price()

    return render_to_response('trader/market_view.html', {'market': market, 'new_order_form': new_order_form,
                                                          'market_price': market_price})


def dashboard(request):
    markets = Market.objects.all()
    recent_orders = Order.objects.all().order_by('-when_created')[0:30]

    return render_to_response('trader/dashboard.html', {'markets': markets, 'recent_orders': recent_orders})


def order_submit(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    market_abbrev = request.POST['market']
    amount = float(request.POST['amount'])
    market_order = ('market_order' in request.POST.keys)
    price = float(request.POST['price'])
    order_type = request.POST['type']

    market = Market.objects.get(abbrev=market_abbrev)
    order = Order()
    order.market = market
    order.amount = amount
    order.type = order_type
    if market_order:
        order.market_order = True
    else:
        order.market_order = False
        order.price = price

    order.save()
    market.market_api.api_execute_order(order)

    return render_to_response('trader/json/success_plain.json',
                              content_type="application/json",
                              context_instance=RequestContext(request))