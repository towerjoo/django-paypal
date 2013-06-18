from django.shortcuts import render, render_to_response
from django.conf import settings
from paypal.digitalgoods.forms import PaypalDGForm
from django.core.urlresolvers import reverse

# Create your views here.
from django.http import HttpResponse


def index(request, template="index.html"):
    notify_url = settings.SITE_DOMAIN + reverse("notify")
    form = PaypalDGForm(initial={
        'amount': 100, 
        'item_name': 'TF2Shop purchase 10 items',
        'invoice': "123",
        'notify_url': notify_url,
        'return_url': settings.SITE_DOMAIN + reverse('return'),
        'cancel_return': settings.SITE_DOMAIN + reverse('cancel'),
    })
    return render_to_response(template, {"form" : form})

def notify(request):
    import os
    f = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log.txt")
    fh = open(f, "w+")
    fh.write(request.GET)
    fh.close()
    

def return_(request):
    out = """<script>
    if (window.opener){
    window.close();
    }
    else if (top.dg.isOpen() == true){
    top.dg.closeFlow();
    }
    </script><h2>Returned</h2>"""
    return HttpResponse(out)

def cancel(request):
    out = """<script>
    if (window.opener){
    window.close();
    }
    else if (top.dg.isOpen() == true){
    top.dg.closeFlow();
    }
    </script><h2>canceled</h2>"""
    return HttpResponse(out)
