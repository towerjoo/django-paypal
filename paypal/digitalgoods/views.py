#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from paypal.digitalgoods.forms import PaypalDGForm
from paypal.digitalgoods.handler import paypal_handler
 
 
@require_POST
@csrf_exempt
def dg(request):
    """
    PayPal IPN endpoint (notify_url).
    Used by both PayPal Payments Pro and Payments Standard to confirm transactions.
    http://tinyurl.com/d9vu9d
    
    PayPal IPN Simulator:
    https://developer.paypal.com/cgi-bin/devscr?cmd=_ipn-link-session
    """
    #data = request.POST.copy()
    #import pdb;pdb.set_trace()
    form = PaypalDGForm(request.POST)
    if form.is_valid():
        flag, url = form.set_express_checkout()
        if flag:
            return HttpResponseRedirect(url)
    return HttpResponse("ERROR")
