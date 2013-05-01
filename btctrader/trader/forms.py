from django.forms import ModelForm
from models import Order


class NewOrderForm(ModelForm):
    """
    Used for creating a NEW order - i.e. not editing an existing one
    Therefore some fields are omitted
    """

    class Meta:
        model = Order
        exclude = ('status', 'market_order_id')