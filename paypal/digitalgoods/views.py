#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from paypal.digitalgoods.forms import PaypalDGForm
 
 
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
    data = request.POST.copy()
    form = PaypalDGForm(data)
    import pdb;pdb.set_trace()
    if form.is_valid():
        pass

    return HttpResponse("OKAY")
