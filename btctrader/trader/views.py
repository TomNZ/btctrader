from django.shortcuts import render_to_response
from markets import MtGoxMarket

def index(request):
    mtgox = MtGoxMarket()
    fee = mtgox.get_trade_fee()
    return render_to_response('index.html', {'data' : fee})