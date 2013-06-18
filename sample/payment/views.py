from django.shortcuts import render, render_to_response
from django.conf import settings
from paypal.digitalgoods.forms import PaypalDGForm
from django.core.urlresolvers import reverse

# Create your views here.
from django.http import HttpResponse


def index(request, template="index.html"):
    notify_url = settings.SITE_DOMAIN + "/__paypal/dg/"
    form = PaypalDGForm(initial={
        'amount': 100, 
        'item_name': 'TF2Shop purchase 10 items',
        'invoice': "123",
        'notify_url': notify_url,
        'return_url': settings.SITE_DOMAIN + reverse('return'),
        'cancel_return': settings.SITE_DOMAIN + reverse('cancel'),
        'charset': 'utf-8',
        'no_shipping': 0
    })
    return render_to_response(template, {"form" : form})

def return_(request):
    pass

def cancel(request):
    pass
