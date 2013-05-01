from django.shortcuts import render_to_response
import markets
import forms


def index(request):
    orderform = forms.NewOrderForm()

    # Was there a postback?
    # TODO: Handle the postback

    return render_to_response('index.html', {'orderform' : orderform})