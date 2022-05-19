import json
# import paystack

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .cart import Cart

from order.models import Order
from store.utilities import decrement_product_quantity, send_order_confirmation

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    paystack.api_key = settings.PAYSTACK_API_KEY_HIDDEN

    try:
        event = paystack.Event.construct_from(
            json.loads(payload), paystack.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        
        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid = True
        order.save()

        decrement_product_quantity(order)  
        send_order_confirmation(order)
        
    return HttpResponse(status=200)